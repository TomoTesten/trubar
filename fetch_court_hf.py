#!/usr/bin/env python3
"""
T.R.U.B.A.R. — Court decisions → Hugging Face Dataset

Fetches all Slovenian court decisions and pushes them as a HF dataset
instead of committing to git (which would blow GitHub's size limits).

Sources:
  - PISRS sodna praksa (228k): Vrhovno, Upravno, VDSS, višja sodišča
  - Ustavno sodišče (25.8k): us-rs.si JSON API + HTML scraping

Output: huggingface.co/datasets/{HF_REPO}
  - split "sodna_praksa" — PISRS decisions
  - split "ustavno_sodisce" — Constitutional Court decisions

Usage:
  python fetch_court_hf.py --hf-repo TomoTesten/trubar-sodna-praksa
  python fetch_court_hf.py --hf-repo TomoTesten/trubar-sodna-praksa --only-us-rs
  python fetch_court_hf.py --hf-repo TomoTesten/trubar-sodna-praksa --dry-run

Requires: HF_TOKEN env var or ~/.hf_token file (write access to the repo).
"""

import json, re, os, time, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import threading
import pyarrow as pa
import pyarrow.parquet as pq

import requests
from bs4 import BeautifulSoup
from huggingface_hub import HfApi, create_repo

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch import REPO_DIR
from fetch_pisrs import (
    pisrs_years, pisrs_items_for_year, _pisrs_cursor_pages,
    item_date, safe_name, PISRS_HEADERS, PISRS_RESULT,
    fetch_pisrs_npb,
)
from fetch_us_rs import fetch_all_urls, fetch_decision, US_RS_BASE

TODAY      = date.today().isoformat()
CACHE_DIR  = REPO_DIR / ".court_hf_cache"
_SAFE_RE   = re.compile(r"[^a-zA-Z0-9_-]")
_local     = threading.local()
_prog_lock = threading.Lock()

PISRS_COURT_ZBIRKE = [
    "Sodna praksa Vrhovnega sodišča",
    "Sodna praksa Upravnega sodišča",
    "Sodna praksa Višjega delovnega in socialnega sodišča",
    "Sodna praksa višjih sodišč",
]

# Arrow schema for both splits
SCHEMA_SP = pa.schema([
    ("id",       pa.string()),
    ("zbirka",   pa.string()),
    ("datum",    pa.string()),
    ("sop",      pa.string()),
    ("naziv",    pa.string()),
    ("organ",    pa.string()),
    ("status",   pa.string()),
    ("vir",      pa.string()),
    ("text",     pa.string()),
])

SCHEMA_US = pa.schema([
    ("id",               pa.string()),
    ("opravilna_st",     pa.string()),
    ("datum",            pa.string()),
    ("ecli",             pa.string()),
    ("vrsta_zadeve",     pa.string()),
    ("vrsta_odlocitve",  pa.string()),
    ("vrsta_resitve",    pa.string()),
    ("vlagatelj",        pa.string()),
    ("vir",              pa.string()),
    ("text",             pa.string()),
])

BATCH_SIZE = 2000  # records per Parquet shard


# ── HF helpers ────────────────────────────────────────────────────────────────

def get_hf_token():
    token = os.environ.get("HF_TOKEN") or ""
    if not token:
        tf = Path.home() / ".hf_token"
        if tf.exists():
            token = tf.read_text().strip()
    if not token:
        raise RuntimeError("Set HF_TOKEN env var or create ~/.hf_token")
    return token


def ensure_hf_repo(repo_id, token):
    try:
        create_repo(repo_id, repo_type="dataset", token=token, exist_ok=True)
        print(f"HF repo ready: {repo_id}")
    except Exception as e:
        print(f"Warning: could not create/verify repo: {e}")


def upload_parquet(api, repo_id, local_path, repo_path, token):
    api.upload_file(
        path_or_fileobj=str(local_path),
        path_in_repo=repo_path,
        repo_id=repo_id,
        repo_type="dataset",
        token=token,
    )


# ── Progress ──────────────────────────────────────────────────────────────────

def progress_file(name):
    return REPO_DIR / f".progress_court_hf_{_SAFE_RE.sub('_', name)[:30]}.txt"


def load_progress(name):
    pf = progress_file(name)
    return set(pf.read_text().splitlines()) if pf.exists() else set()


def save_progress(name, item_id):
    with _prog_lock:
        with open(progress_file(name), "a") as f:
            f.write(item_id + "\n")


# ── PISRS sodna praksa fetcher ─────────────────────────────────────────────────

_SODNAPRAKSA_URL = (
    "https://sodnapraksa.si/?q=id:{id}"
    "&database[SOVS]=SOVS&database[IESP]=IESP"
    "&database[VDSS]=VDSS&database[UPRS]=UPRS"
    "&_submit=išči&page=0&id={id}"
)
_SP_SKIP = frozenset({"Priljubljeni dokumenti", "Nastavitve", "Pomoč", "Iskalnik sodne prakse"})
_DOC_RE  = re.compile(r"doc_(\d+)$")


def _session():
    if not hasattr(_local, "s"):
        s = requests.Session()
        s.headers.update({"User-Agent": PISRS_HEADERS["User-Agent"]})
        _local.s = s
    return _local.s


def fetch_sp_text(zunanji_id):
    m = _DOC_RE.match(zunanji_id)
    if not m:
        return None
    doc_id = m.group(1)
    url    = _SODNAPRAKSA_URL.format(id=doc_id)
    for attempt in range(3):
        try:
            r = _session().get(url, timeout=20)
            if r.status_code != 200:
                return None
            soup = BeautifulSoup(r.text, "lxml")
            for tag in soup.find_all(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            container = soup.find(id="container") or soup.find("body") or soup
            lines = [l.strip() for l in container.get_text(separator="\n").split("\n")
                     if len(l.strip()) > 40]
            lines = [l for l in lines if l not in _SP_SKIP]
            return "\n\n".join(lines) if len(lines) > 3 else None
        except Exception:
            if attempt == 2:
                return None
            time.sleep(2 ** attempt)
    return None


def fetch_sp_record(item):
    zid   = item.get("zunanjiId", "")
    text  = fetch_sp_text(zid)
    if not text:
        return None
    return {
        "id":     zid,
        "zbirka": item.get("nazivZbirke", ""),
        "datum":  item_date(item),
        "sop":    item.get("sop") or "",
        "naziv":  item.get("nazivAkta") or "",
        "organ":  item.get("organSprejemaAliIzdaje") or "",
        "status": (item.get("semafor") or {}).get("naziv") or "",
        "vir":    f"https://sodnapraksa.si/?q=id:{_DOC_RE.match(zid).group(1)}" if _DOC_RE.match(zid) else "",
        "text":   text,
    }


def build_sp_index(zbirka):
    cache = REPO_DIR / f".index_{_SAFE_RE.sub('_', zbirka)[:40]}.json"
    if cache.exists():
        items = json.loads(cache.read_text())
        print(f"  Loaded {len(items)} items from cache")
        return items
    print(f"  Fetching index for '{zbirka}'...")
    years = pisrs_years(zbirka)
    items, seen = [], set()
    for year, count in years:
        for item in pisrs_items_for_year(zbirka, year):
            zid = item.get("zunanjiId", "")
            if zid and zid not in seen:
                items.append(item)
                seen.add(zid)
    cache.write_text(json.dumps(items))
    print(f"  Cached {len(items)} items")
    return items


def run_sp_collection(zbirka, api, repo_id, token, workers, dry_run):
    print(f"\n=== {zbirka} ===")
    items   = build_sp_index(zbirka)
    done    = load_progress(zbirka)
    pending = [it for it in items if it.get("zunanjiId", "") and it["zunanjiId"] not in done]
    print(f"  {len(pending)} pending, {len(done)} already done")

    CACHE_DIR.mkdir(exist_ok=True)
    shard_prefix = _SAFE_RE.sub("_", zbirka)[:30]

    buffer     = []
    shard_idx  = sum(1 for f in CACHE_DIR.glob(f"{shard_prefix}_*.parquet"))
    ok = fail  = 0
    total      = len(pending)

    def flush(buf, idx):
        path = CACHE_DIR / f"{shard_prefix}_{idx:04d}.parquet"
        table = pa.Table.from_pylist(buf, schema=SCHEMA_SP)
        pq.write_table(table, str(path), compression="zstd")
        if not dry_run:
            hf_path = f"data/sodna_praksa/{shard_prefix}_{idx:04d}.parquet"
            upload_parquet(api, repo_id, path, hf_path, token)
            print(f"  → uploaded shard {idx} ({len(buf)} records)")
        return idx + 1

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(fetch_sp_record, it): it for it in pending}
        done_n  = 0
        for future in as_completed(futures):
            item   = futures[future]
            zid    = item.get("zunanjiId", "")
            done_n += 1
            try:
                rec = future.result()
            except Exception as e:
                rec = None
            if rec:
                buffer.append(rec)
                ok += 1
            else:
                fail += 1
            save_progress(zbirka, zid)

            if done_n % 500 == 0:
                print(f"  [{done_n}/{total}] ok={ok} fail={fail}")

            if len(buffer) >= BATCH_SIZE:
                shard_idx = flush(buffer, shard_idx)
                buffer = []

    if buffer:
        shard_idx = flush(buffer, shard_idx)

    print(f"  Done: {ok} ok, {fail} no-text")
    return ok


# ── Constitutional Court ───────────────────────────────────────────────────────

def run_us_rs(api, repo_id, token, workers, dry_run):
    print("\n=== Ustavno sodišče RS ===")
    all_urls = fetch_all_urls()
    done     = load_progress("us_rs")
    pending  = [u for u in all_urls if u.rstrip("/").split("/")[-1] not in done]
    print(f"  {len(pending)} pending, {len(done)} already done")

    CACHE_DIR.mkdir(exist_ok=True)
    buffer    = []
    shard_idx = sum(1 for f in CACHE_DIR.glob("us_rs_*.parquet"))
    ok = fail = 0
    total     = len(pending)

    def flush(buf, idx):
        path = CACHE_DIR / f"us_rs_{idx:04d}.parquet"
        table = pa.Table.from_pylist(buf, schema=SCHEMA_US)
        pq.write_table(table, str(path), compression="zstd")
        if not dry_run:
            upload_parquet(api, repo_id, path, f"data/ustavno_sodisce/us_rs_{idx:04d}.parquet", token)
            print(f"  → uploaded shard {idx} ({len(buf)} records)")
        return idx + 1

    with ThreadPoolExecutor(max_workers=workers) as ex:
        futures = {ex.submit(fetch_decision, url): url for url in pending}
        done_n  = 0
        for future in as_completed(futures):
            url  = futures[future]
            slug = url.rstrip("/").split("/")[-1]
            done_n += 1
            try:
                result = future.result()
            except Exception:
                result = None

            if result:
                _, meta, text = result
                buffer.append({
                    "id":              slug,
                    "opravilna_st":    meta.get("opravilna_st", ""),
                    "datum":           meta.get("datum", ""),
                    "ecli":            meta.get("ecli", ""),
                    "vrsta_zadeve":    meta.get("vrsta_zadeve", ""),
                    "vrsta_odlocitve": meta.get("vrsta_odlocitve", ""),
                    "vrsta_resitve":   meta.get("vrsta_resitve", ""),
                    "vlagatelj":       meta.get("vlagatelj", ""),
                    "vir":             url,
                    "text":            text,
                })
                ok += 1
            else:
                fail += 1
            save_progress("us_rs", slug)

            if done_n % 500 == 0:
                print(f"  [{done_n}/{total}] ok={ok} fail={fail}")

            if len(buffer) >= BATCH_SIZE:
                shard_idx = flush(buffer, shard_idx)
                buffer = []

    if buffer:
        shard_idx = flush(buffer, shard_idx)

    print(f"  Done: {ok} ok, {fail} failed")
    return ok


# ── Dataset card ──────────────────────────────────────────────────────────────

README = """\
---
language:
- sl
license: cc0-1.0
tags:
- legal
- slovenian
- court-decisions
pretty_name: "T.R.U.B.A.R. — Sodna praksa"
size_categories:
- 100K<n<1M
---

# T.R.U.B.A.R. — Sodna praksa

Slovenian court decisions as a machine-readable dataset, part of the
[T.R.U.B.A.R.](https://github.com/TomoTesten/trubar) project
(*Transparentni Register Urejenih Besedil Aktov Republike Slovenije*).

## Contents

| Split | Source | Records |
|---|---|---|
| `sodna_praksa` | PISRS / sodnapraksa.si | ~228k |
| `ustavno_sodisce` | Ustavno sodišče RS (us-rs.si) | ~25.8k |

## Usage

```python
from datasets import load_dataset

# All court decisions
ds = load_dataset("TomoTesten/trubar-sodna-praksa", "sodna_praksa")

# Constitutional Court only
ds = load_dataset("TomoTesten/trubar-sodna-praksa", "ustavno_sodisce")
```

## Fields

**sodna_praksa**: `id`, `zbirka`, `datum`, `sop`, `naziv`, `organ`, `status`, `vir`, `text`

**ustavno_sodisce**: `id`, `opravilna_st`, `datum`, `ecli`, `vrsta_zadeve`,
`vrsta_odlocitve`, `vrsta_resitve`, `vlagatelj`, `vir`, `text`

## License

CC0 1.0 — public domain. Source texts are official public records of the
Republic of Slovenia.
"""


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--hf-repo",    default="TomoTesten/trubar-sodna-praksa")
    parser.add_argument("--workers",    type=int, default=12)
    parser.add_argument("--dry-run",    action="store_true",
                        help="Fetch and cache locally but don't upload to HF")
    parser.add_argument("--only-us-rs", action="store_true",
                        help="Only fetch Constitutional Court decisions")
    parser.add_argument("--only-pisrs", action="store_true",
                        help="Only fetch PISRS sodna praksa")
    args = parser.parse_args()

    token = None if args.dry_run else get_hf_token()
    api   = HfApi() if not args.dry_run else None

    if not args.dry_run:
        ensure_hf_repo(args.hf_repo, token)
        # Upload dataset card
        api.upload_file(
            path_or_fileobj=README.encode(),
            path_in_repo="README.md",
            repo_id=args.hf_repo,
            repo_type="dataset",
            token=token,
        )

    total_ok = 0

    if not args.only_us_rs:
        for zbirka in PISRS_COURT_ZBIRKE:
            total_ok += run_sp_collection(
                zbirka, api, args.hf_repo, token, args.workers, args.dry_run
            )

    if not args.only_pisrs:
        total_ok += run_us_rs(api, args.hf_repo, token, args.workers, args.dry_run)

    print(f"\n=== All done. {total_ok} records pushed to {args.hf_repo} ===")


if __name__ == "__main__":
    main()
