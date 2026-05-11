#!/usr/bin/env python3
"""
T.R.U.B.A.R. — Veljavni akti lokalnih skupnosti → Hugging Face Dataset

Fetches ~107k valid municipal ordinances (odloki, pravilniki, sklepi) from
PISRS and uploads as Parquet shards to HuggingFace.

Pagination strategy: region × year (11 regions × ~45 years ≈ 440 queries,
each well under the ~1000-item cursor cap).

Text source: Uradni list RS (same SOP-based URLs as national laws).

Usage:
  python fetch_ls.py --hf-repo TomoTesten/trubar-lokalne-skupnosti --workers 8
  python fetch_ls.py --hf-repo TomoTesten/trubar-lokalne-skupnosti --dry-run
"""

import json, re, os, time, argparse, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import requests
import pyarrow as pa
import pyarrow.parquet as pq
from huggingface_hub import HfApi, create_repo

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch import REPO_DIR, html_to_markdown, fetch_ul_html

PISRS_FILTER = "https://pisrs.si/api/filter/filter"
PISRS_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
}
ZBIRKA   = "Veljavni akti lokalnih skupnosti"
BATCH_SIZE = 2000
CACHE_DIR  = REPO_DIR / ".ls_hf_cache"
_SAFE_RE   = re.compile(r"[^a-zA-Z0-9_-]")
_prog_lock = threading.Lock()
_local     = threading.local()

SCHEMA = pa.schema([
    ("id",     pa.string()),
    ("naziv",  pa.string()),
    ("organ",  pa.string()),
    ("regija", pa.string()),
    ("datum",  pa.string()),
    ("sop",    pa.string()),
    ("vir",    pa.string()),
    ("text",   pa.string()),
])


# ── HF helpers ────────────────────────────────────────────────────────────────

def get_hf_token():
    token = os.environ.get("HF_TOKEN") or ""
    if not token:
        tf = Path.home() / ".hf_token"
        if tf.exists():
            token = tf.read_text().strip()
    if not token:
        raise RuntimeError("Set HF_TOKEN or create ~/.hf_token")
    return token


def ensure_hf_repo(repo_id, token):
    try:
        create_repo(repo_id, repo_type="dataset", token=token, exist_ok=True)
        print(f"HF repo ready: {repo_id}")
    except Exception as e:
        print(f"Warning: {e}")


def upload_parquet(api, repo_id, local_path, repo_path, token):
    api.upload_file(
        path_or_fileobj=str(local_path),
        path_in_repo=repo_path,
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
    )


# ── Progress ──────────────────────────────────────────────────────────────────

PROGRESS_FILE = REPO_DIR / ".progress_ls_hf.txt"

def load_progress():
    return set(PROGRESS_FILE.read_text().splitlines()) if PROGRESS_FILE.exists() else set()

def save_progress(sop):
    with _prog_lock:
        with open(PROGRESS_FILE, "a") as f:
            f.write(sop + "\n")


# ── PISRS pagination ──────────────────────────────────────────────────────────

def pisrs_post(params, body, retries=5):
    for attempt in range(retries):
        try:
            resp = requests.post(PISRS_FILTER, headers=PISRS_HEADERS,
                                 params=params, json=body, timeout=30)
            resp.raise_for_status()
            return resp.json().get("data") or {}
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    return {}


def get_regions():
    """Return list of (region_name, count) tuples."""
    data = pisrs_post({"cursorMark": "*"}, {"nazivZbirke": [ZBIRKA]})
    return [(f["value"], f["count"])
            for f in data.get("regijaOrganSprejetjaFacet", [])
            if f.get("value")]


def get_years():
    """Return sorted list of years with at least 1 item."""
    data = pisrs_post({"cursorMark": "*"}, {"nazivZbirke": [ZBIRKA]})
    return sorted([f["value"] for f in data.get("letoObjaveFacet", [])
                   if isinstance(f.get("value"), int)])


def items_for_region_year(region, year):
    """Cursor-paginate all items for a region+year combination."""
    cursor = "*"
    while True:
        data = pisrs_post({"cursorMark": cursor}, {
            "nazivZbirke": [ZBIRKA],
            "regijaOrganSprejetja": [region],
            "datumi": {"letoObjave": year},
        })
        items = data.get("seznam") or []
        if not items:
            break
        yield from items
        nc = data.get("nextCursorMark", cursor)
        if nc == cursor:
            break
        cursor = nc
        time.sleep(0.1)


# ── Text fetching ─────────────────────────────────────────────────────────────

def _session():
    if not hasattr(_local, "s"):
        s = requests.Session()
        s.headers.update({"User-Agent": PISRS_HEADERS["User-Agent"]})
        _local.s = s
    return _local.s


def fetch_text(sop):
    """Fetch and convert law text from Uradni list RS."""
    if not sop:
        return None
    url = f"https://www.uradni-list.si/1/objava.jsp?sop={sop}"
    for attempt in range(3):
        try:
            r = _session().get(url, timeout=25)
            if r.status_code == 404:
                return None
            if r.status_code != 200:
                time.sleep(2 ** attempt)
                continue
            md = html_to_markdown(r.text)
            return md if md and len(md) > 100 else None
        except Exception:
            if attempt == 2:
                return None
            time.sleep(2 ** attempt)
    return None


def fetch_record(item):
    sop  = item.get("sop") or ""
    text = fetch_text(sop)
    if not text:
        return None
    datum = (item.get("datumObjave") or item.get("datumSprejetja") or "")[:10]
    regija_raw = ""
    return {
        "id":     sop or item.get("interniId", ""),
        "naziv":  item.get("nazivAkta") or "",
        "organ":  item.get("organSprejemaAliIzdaje") or "",
        "regija": "",  # filled by caller
        "datum":  datum,
        "sop":    sop,
        "vir":    f"https://www.uradni-list.si/1/objava.jsp?sop={sop}" if sop else "",
        "text":   text,
    }


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--hf-repo", default="TomoTesten/trubar-lokalne-skupnosti")
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    token = get_hf_token()
    api   = HfApi()
    if not args.dry_run:
        ensure_hf_repo(args.hf_repo, token)

    CACHE_DIR.mkdir(exist_ok=True)

    print("Loading regions and years...")
    regions = get_regions()
    years   = get_years()
    print(f"  {len(regions)} regions, {len(years)} years ({years[0]}–{years[-1]})")

    done    = load_progress()
    buffer  = []
    shard_n = sum(1 for f in CACHE_DIR.glob("ls_*.parquet"))
    total_ok = 0

    def flush(buf, idx):
        path = CACHE_DIR / f"ls_{idx:04d}.parquet"
        tbl  = pa.Table.from_pylist(buf, schema=SCHEMA)
        pq.write_table(tbl, str(path), compression="zstd")
        if not args.dry_run:
            upload_parquet(api, args.hf_repo, path,
                           f"data/lokalne_skupnosti/ls_{idx:04d}.parquet", token)
            print(f"  → uploaded shard {idx} ({len(buf)} records)")
        return idx + 1

    for regija, reg_count in regions:
        reg_name = regija.split("#")[0]
        print(f"\n=== {reg_name} ({reg_count} total) ===")
        reg_ok = reg_fail = 0

        for year in years:
            batch_items = list(items_for_region_year(regija, year))
            pending = [it for it in batch_items
                       if (it.get("sop") or str(it.get("interniId", ""))) not in done]
            if not pending:
                continue

            with ThreadPoolExecutor(max_workers=args.workers) as ex:
                futures = {}
                for it in pending:
                    f = ex.submit(fetch_record, it)
                    futures[f] = it

                for future in as_completed(futures):
                    it  = futures[future]
                    sop = it.get("sop") or str(it.get("interniId", ""))
                    try:
                        rec = future.result()
                    except Exception:
                        rec = None
                    if rec:
                        rec["regija"] = reg_name
                        buffer.append(rec)
                        reg_ok += 1
                        total_ok += 1
                    else:
                        reg_fail += 1
                    save_progress(sop)

                    if len(buffer) >= BATCH_SIZE:
                        shard_n = flush(buffer, shard_n)
                        buffer = []

        print(f"  {reg_name}: {reg_ok} ok, {reg_fail} no-text")

    if buffer:
        shard_n = flush(buffer, shard_n)

    print(f"\n=== All done. {total_ok} records pushed to {args.hf_repo} ===")


if __name__ == "__main__":
    main()
