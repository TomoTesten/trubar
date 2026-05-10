#!/usr/bin/env python3
"""
T.R.U.B.A.R. — general PISRS collection fetcher (optimized)

Fetches any named PISRS collection year-by-year, downloads text from
Uradni list RS (or PISRS NPB as fallback), and commits to git.

Usage:
  python fetch_pisrs.py --zbirka "Veljavni akti lokalnih skupnosti" [--delay 0.3]
  python fetch_pisrs.py --zbirka "Drugi splošni in posamični akti"
  python fetch_pisrs.py --zbirka "Splošni akti za izvrševanje javnih pooblastil"

Items are stored in si/{safe_zunanjiId}.md  (same directory as other predpisi).
Progress is tracked per-collection in .progress_{safe_name}.txt (append-only).
"""

import json, re, os, time, argparse, subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import date
from pathlib import Path
import threading

import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch import html_to_markdown, fetch_ul_html, REPO_DIR, LAW_DIR

PISRS_FILTER  = "https://pisrs.si/api/filter/filter"
PISRS_RESULT  = "https://pisrs.si/api/rezultat"
PISRS_HEADERS = {"Content-Type": "application/json",
                 "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}
UL_BASE       = "https://www.uradni-list.si/1/objava.jsp?sop={sop}"
TODAY         = date.today().isoformat()

VRSTA_MAP = {
    "URED": "uredba", "PRAV": "pravilnik", "ODRE": "odredba",
    "NAVO": "navodilo", "SKLE": "sklep", "ODLO": "odlok",
    "DRUG": "drugi akt", "AKT": "akt", "MP_ODLO": "občinski odlok",
    "MP_SKLE": "občinski sklep", "MP_PRAV": "občinski pravilnik",
    "MP_NAWO": "občinsko navodilo",
    "doc_": "sodna odločba",
}

SODNAPRAKSA_URL = ("https://sodnapraksa.si/?q=id:{id}"
                   "&database[SOVS]=SOVS&database[IESP]=IESP"
                   "&database[VDSS]=VDSS&database[UPRS]=UPRS"
                   "&_submit=išči&page=0&id={id}")

# Module-level compiled regexes
_SAFE_RE    = re.compile(r"[^a-zA-Z0-9_-]")
_DATE_RE    = re.compile(r"\d{4}-\d{2}-\d{2}")
_YEAR_RE    = re.compile(r"(\d{4})-")
_DOC_RE     = re.compile(r"doc_(\d+)$")

# Thread-local sessions
_local = threading.local()

def _session():
    if not hasattr(_local, "session"):
        s = requests.Session()
        s.headers.update({"User-Agent": PISRS_HEADERS["User-Agent"]})
        _local.session = s
    return _local.session

# Shared session for PISRS API (not thread-local — only used in main thread for index building)
_api_session = requests.Session()
_api_session.headers.update(PISRS_HEADERS)


# ── PISRS API helpers ──────────────────────────────────────────────────────────

def pisrs_post(params, body, retries=5):
    for attempt in range(retries):
        try:
            r = _api_session.post(PISRS_FILTER, params=params, json=body, timeout=30)
            r.raise_for_status()
            return r.json().get("data") or {}
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    return {}


def pisrs_get(url, retries=4):
    for attempt in range(retries):
        try:
            r = _session().get(url, timeout=20)
            if r.status_code == 200:
                return r.json().get("data")
            if r.status_code == 404:
                return None
        except Exception:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    return None


def pisrs_years(zbirka):
    data = pisrs_post({"cursorMark": "*"}, {"nazivZbirke": [zbirka]})
    return [(f["value"], f["count"])
            for f in (data.get("letoObjaveFacet") or [])
            if isinstance(f.get("value"), int)]


def pisrs_items_for_year(zbirka, year):
    cursor = "*"
    while True:
        data  = pisrs_post({"cursorMark": cursor},
                           {"nazivZbirke": [zbirka], "datumi": {"letoObjave": year}})
        items = data.get("seznam") or []
        if not items:
            break
        yield from items
        nc = data.get("nextCursorMark", cursor)
        if nc == cursor:
            break
        cursor = nc
        time.sleep(0.03)


def _pisrs_cursor_pages(body):
    cursor = "*"
    while True:
        data  = pisrs_post({"cursorMark": cursor}, body)
        items = data.get("seznam") or []
        if not items:
            break
        yield from items
        nc = data.get("nextCursorMark", cursor)
        if nc == cursor:
            break
        cursor = nc
        time.sleep(0.03)


def pisrs_items_by_municipality(zbirka, municipalities):
    for muni_val, count in municipalities:
        muni_id = muni_val.split("#")[1] if "#" in muni_val else muni_val
        base_body = {"nazivZbirke": [zbirka], "obcinaOrganSprejetjaOrgan": [muni_id]}
        if count <= 900:
            yield from _pisrs_cursor_pages(base_body)
        else:
            for year in range(1945, date.today().year + 2):
                body = dict(base_body)
                body["datumi"] = {"letoSprejetja": year}
                yield from _pisrs_cursor_pages(body)
        time.sleep(0.03)


# ── NPB fallback ───────────────────────────────────────────────────────────────

_HEADS = {"naslov": "##", "clen": "###", "tocka": "####", "podnaslov": "###",
          "naslovDela": "##", "naslovPoglavja": "##"}

def html_blocks_to_markdown(blocks):
    def strip(html):
        return BeautifulSoup(html or "", "lxml").get_text(separator=" ", strip=True)
    lines = []
    for b in blocks:
        s, txt = b.get("struktura", ""), strip(b.get("vsebina", ""))
        if not txt:
            continue
        if s in _HEADS:
            lines.append(f"\n{_HEADS[s]} {txt}\n")
        elif s == "alineja":
            lines.append(f"- {txt}")
        elif s == "opozorilo":
            lines.append(f"> {txt}")
        else:
            lines.append(txt)
    return "\n".join(lines).strip()


def fetch_pisrs_npb(zunanji_id):
    data = pisrs_get(f"{PISRS_RESULT}/zbirka/id/{zunanji_id}")
    if not data:
        return None
    versions = (data.get("besedilo") or {}).get("npbVerzije") or []
    if not versions:
        return None
    active = [v for v in versions if not v.get("datumZacetkaUporabe")
              or v["datumZacetkaUporabe"] <= TODAY]
    current = (active or versions)[-1]
    detail = pisrs_get(f"{PISRS_RESULT}/neuradno-precisceno-besedilo/{current['id']}/details")
    if not detail:
        return None
    blocks = detail.get("besedilo") or []
    return html_blocks_to_markdown(blocks) if blocks else None


# ── Sodna praksa fetcher ───────────────────────────────────────────────────────

_SP_SKIP = frozenset({"Priljubljeni dokumenti", "Nastavitve", "Pomoč", "Iskalnik sodne prakse"})

def fetch_sodna_praksa(zunanji_id):
    m = _DOC_RE.match(zunanji_id)
    if not m:
        return None
    doc_id = m.group(1)
    url = SODNAPRAKSA_URL.format(id=doc_id)
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


# ── File helpers ───────────────────────────────────────────────────────────────

def safe_name(s):
    return _SAFE_RE.sub("_", s)


def item_date(item):
    for f in ("datumObjave", "datumSprejetja"):
        d = item.get(f) or ""
        if _DATE_RE.match(d):
            return d
    sop = item.get("sop") or ""
    m   = _YEAR_RE.match(sop)
    return f"{m.group(1)}-07-01" if m else "2000-07-01"


def make_frontmatter(item):
    def esc(s): return (s or "").replace('"', '\\"')
    zid   = item.get("zunanjiId", "")
    prefix = next((k for k in sorted(VRSTA_MAP, key=len, reverse=True)
                   if zid.startswith(k) and k != "doc_"), "")
    if not prefix and zid.startswith("doc_"):
        prefix = "doc_"
    vrsta = VRSTA_MAP.get(prefix, "akt")
    sop   = item.get("sop") or ""
    return (
        "---\n"
        f"kratica: {zid}\n"
        f'naziv: "{esc(item.get("nazivAkta"))}"\n'
        f'vrsta: "{vrsta}"\n'
        f"datum: {item_date(item)}\n"
        f"sop: {sop}\n"
        f'organ: "{esc(item.get("organSprejemaAliIzdaje"))}"\n'
        f'zbirka: "{esc(item.get("nazivZbirke"))}"\n'
        f'status: "{esc((item.get("semafor") or {}).get("naziv"))}"\n'
        f'vir: "{UL_BASE.format(sop=sop) if sop else ""}"\n'
        "---\n"
    )


# ── Git plumbing (fast batch commits, no working-tree scan) ───────────────────

_GIT_ENV_BASE = {**os.environ}

_git_lock = threading.Lock()


def _git(args, env=None, capture=True):
    return subprocess.run(
        ["git"] + args,
        cwd=str(REPO_DIR),
        env=env or _GIT_ENV_BASE,
        check=True,
        capture_output=capture,
        text=True,
    )


def git_stage_file(filepath):
    rel  = str(filepath.relative_to(REPO_DIR))
    blob = _git(["hash-object", "-w", str(filepath)]).stdout.strip()
    _git(["update-index", "--add", "--cacheinfo", f"100644,{blob},{rel}"])


_MIN_GIT_DATE = "1970-01-02"  # git commit-tree rejects pre-epoch dates

def git_commit_plumbing(date_str, message):
    if date_str < _MIN_GIT_DATE:
        date_str = _MIN_GIT_DATE
    iso = f"{date_str}T12:00:00+01:00"
    env = {**_GIT_ENV_BASE, "GIT_AUTHOR_DATE": iso, "GIT_COMMITTER_DATE": iso}
    tree   = _git(["write-tree"], env=env).stdout.strip()
    parent = _git(["rev-parse", "HEAD"], env=env).stdout.strip()
    commit = _git(["commit-tree", tree, "-p", parent, "-m", message or " "], env=env).stdout.strip()
    _git(["update-ref", "HEAD", commit], env=env)


# ── Progress (append-only text file) ──────────────────────────────────────────

def progress_file(zbirka):
    return REPO_DIR / f".progress_{safe_name(zbirka)[:40]}.txt"


def load_progress(zbirka):
    pf = progress_file(zbirka)
    return set(pf.read_text().splitlines()) if pf.exists() else set()


_progress_locks = {}
_progress_lock_lock = threading.Lock()

def _get_progress_lock(zbirka):
    with _progress_lock_lock:
        if zbirka not in _progress_locks:
            _progress_locks[zbirka] = threading.Lock()
        return _progress_locks[zbirka]


def save_progress_append(zbirka, zid):
    with _get_progress_lock(zbirka):
        with open(progress_file(zbirka), "a") as f:
            f.write(zid + "\n")


# ── Index cache ────────────────────────────────────────────────────────────────

def index_cache_file(zbirka):
    return REPO_DIR / f".index_{safe_name(zbirka)[:40]}.json"


def build_index(zbirka):
    cf = index_cache_file(zbirka)
    if cf.exists():
        items = json.loads(cf.read_text())
        print(f"Loaded {len(items)} items from cache for '{zbirka}'")
        return items

    print(f"Fetching year list for '{zbirka}'...")
    years = pisrs_years(zbirka)

    items, seen = [], set()

    if years:
        print(f"  {len(years)} years: {years[0][0]}–{years[-1][0]}")
        for year, count in years:
            batch = []
            for item in pisrs_items_for_year(zbirka, year):
                zid = item.get("zunanjiId", "")
                if zid and zid not in seen:
                    batch.append(item)
                    seen.add(zid)
            if batch:
                print(f"  {year}: {len(batch)} (of {count})")
                items.extend(batch)
    else:
        data = pisrs_post({"cursorMark": "*"}, {"nazivZbirke": [zbirka]})
        municipalities = [(f["value"], f["count"])
                         for f in (data.get("obcinaOrganSprejetjaOrganFacet") or [])
                         if f.get("value")]
        if not municipalities:
            print("No years or municipalities found.")
            return []
        print(f"  No year facets — iterating by {len(municipalities)} municipalities")
        for item in pisrs_items_by_municipality(zbirka, municipalities):
            zid = item.get("zunanjiId", "")
            if zid and zid not in seen:
                items.append(item)
                seen.add(zid)
        print(f"  Found {len(items)} unique items via municipality scan")

    cf.write_text(json.dumps(items))
    print(f"Cached {len(items)} items.")
    return items


# ── Fetch worker ───────────────────────────────────────────────────────────────

def fetch_one(item, use_npb_fallback):
    """Fetch text for one item. Returns (item, filepath, content) or (item, None, None)."""
    zid   = item.get("zunanjiId", "")
    sop   = item.get("sop") or ""
    naziv = item.get("nazivAkta", "")
    body  = None

    if zid.startswith("doc_"):
        body = fetch_sodna_praksa(zid)
    else:
        if sop:
            html = fetch_ul_html(sop)
            if html:
                body = html_to_markdown(html)
        if not body and use_npb_fallback:
            body = fetch_pisrs_npb(zid)

    if not body:
        return item, None, None

    filepath = LAW_DIR / f"{safe_name(zid)}.md"
    content  = make_frontmatter(item) + f"\n# {naziv}\n\n{body}\n"
    return item, filepath, content


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zbirka",   required=True, help="PISRS collection name")
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--limit",    type=int,   default=0)
    parser.add_argument("--delay",    type=float, default=0.0,
                        help="Extra delay between fetches (default 0, rarely needed)")
    parser.add_argument("--workers",  type=int,   default=8)
    parser.add_argument("--batch-size", type=int, default=50,
                        help="Commit every N items (default 50)")
    parser.add_argument("--no-ul-fallback-npb", action="store_true",
                        help="Skip PISRS NPB fallback if UL fetch fails")
    args = parser.parse_args()

    LAW_DIR.mkdir(exist_ok=True)
    done  = load_progress(args.zbirka)
    items = build_index(args.zbirka)
    items.sort(key=item_date)

    if args.limit:
        items = items[:args.limit]

    pending = [it for it in items if it.get("zunanjiId", "") and it["zunanjiId"] not in done]
    skipped = len(items) - len(pending)
    print(f"\nProcessing {len(pending)} items (skipping {skipped} already done) from '{args.zbirka}'")
    print(f"Workers: {args.workers}, batch size: {args.batch_size}")

    use_npb = not args.no_ul_fallback_npb
    ok = fail = 0

    # Staged files waiting to be committed, grouped by date
    staged: dict[str, list[str]] = {}   # date_str → list of commit messages
    staged_count = 0

    def flush_staged():
        nonlocal staged, staged_count
        if not staged:
            return
        with _git_lock:
            for date_str in sorted(staged.keys()):
                msgs = staged[date_str]
                combined = msgs[0] if len(msgs) == 1 else f"[batch {date_str}] {len(msgs)} items"
                git_commit_plumbing(date_str, combined)
        staged = {}
        staged_count = 0

    total   = len(pending)
    done_n  = 0

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(fetch_one, item, use_npb): item for item in pending}

        for future in as_completed(futures):
            item = futures[future]
            zid  = item.get("zunanjiId", "")
            done_n += 1

            try:
                _, filepath, content = future.result()
            except Exception as e:
                print(f"[{done_n}/{total}] {zid} → EXCEPTION: {e}")
                fail += 1
                done.add(zid)
                save_progress_append(args.zbirka, zid)
                continue

            if filepath is None:
                print(f"[{done_n}/{total}] {zid} → NO TEXT")
                fail += 1
            else:
                filepath.write_text(content, encoding="utf-8")
                print(f"[{done_n}/{total}] {zid} → OK")
                ok += 1

                if not args.dry_run:
                    d = item_date(item)
                    msg = f"[{zid}] {item.get('nazivAkta', '')}"
                    with _git_lock:
                        try:
                            git_stage_file(filepath)
                            if d not in staged:
                                staged[d] = []
                            staged[d].append(msg)
                            staged_count += 1
                        except Exception as e:
                            print(f"  git stage error: {e}")

            done.add(zid)
            save_progress_append(args.zbirka, zid)

            if args.delay:
                time.sleep(args.delay)

            # Commit batch when ready
            if staged_count >= args.batch_size and not args.dry_run:
                flush_staged()
                print(f"  → committed batch (total ok={ok}, fail={fail})")

    # Final commit for remaining staged files
    if not args.dry_run:
        flush_staged()

    print(f"\nDone: {ok} ok, {skipped} skipped, {fail} no-text")


if __name__ == "__main__":
    main()
