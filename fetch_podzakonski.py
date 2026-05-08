#!/usr/bin/env python3
"""
T.R.U.B.A.R. — fetch podzakonski akti (uredbe, pravilniki, odredbe)

Strategy: iterate PISRS Register predpisov year by year (avoiding the ~1000-item
cursor cap that applies to the unfiltered index). For each year, cursor-paginate
through all items and collect non-ZAKO acts, then fetch their text from Uradni list RS.

Known limitation: year 2023 has 1,279 items; cursor cap yields ~1,000 of them.

Usage:
  python fetch_podzakonski.py [--limit N] [--dry-run] [--delay SEC]
"""

import json, re, os, time, argparse, subprocess
from pathlib import Path

import requests

# Reuse HTML→Markdown and UL-fetch helpers from fetch.py
import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch import html_to_markdown, fetch_ul_html, REPO_DIR, LAW_DIR

PROGRESS_FILE = REPO_DIR / ".progress_podzakonski.json"
PISRS_FILTER  = "https://pisrs.si/api/filter/filter"
UL_BASE       = "https://www.uradni-list.si/1/objava.jsp?sop={sop}"

PISRS_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent":   "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
}

# Skip ZAKO (laws — already in fetch.py) and USTAva/KOLPektivna/etc noise
SKIP_PREFIXES = {"ZAKO", "USTA", "USTZ", "KOLP", "DRUG", "AKT", "STAT", "TARI"}

VRSTA_MAP = {
    "URED": "uredba",
    "PRAV": "pravilnik",
    "ODRE": "odredba",
    "NAVO": "navodilo",
    "SKLE": "sklep",
    "ODLO": "odlok",
    "ODLB": "odlok",
    "ODLU": "odlok",
}


# ── PISRS pagination ───────────────────────────────────────────────────────────

def pisrs_years():
    """Return list of years that have items in Register predpisov."""
    resp = requests.post(PISRS_FILTER, headers=PISRS_HEADERS,
                         params={"cursorMark": "*"},
                         json={"nazivZbirke": ["Register predpisov"]},
                         timeout=30)
    data = resp.json().get("data") or {}
    return [(f["value"], f["count"])
            for f in data.get("letoObjaveFacet", [])
            if isinstance(f.get("value"), int)]


def pisrs_items_for_year(year):
    """Yield all Register predpisov items for a given year (up to ~1000)."""
    cursor = "*"
    while True:
        resp = requests.post(PISRS_FILTER, headers=PISRS_HEADERS,
                             params={"cursorMark": cursor},
                             json={"nazivZbirke": ["Register predpisov"],
                                   "datumi": {"letoObjave": year}},
                             timeout=30)
        data  = resp.json().get("data") or {}
        items = data.get("seznam") or []
        if not items:
            break
        yield from items
        nc = data.get("nextCursorMark", cursor)
        if nc == cursor:
            break
        cursor = nc
        time.sleep(0.08)


def wanted(item):
    zid = item.get("zunanjiId", "")
    prefix = "".join(c for c in zid if c.isalpha())
    return prefix not in SKIP_PREFIXES and bool(zid)


# ── File helpers ───────────────────────────────────────────────────────────────

def item_filename(item):
    zid  = item.get("zunanjiId") or item.get("sop", "UNKNOWN")
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", zid)
    return f"{safe}.md"


def item_date(item):
    for field in ("datumObjave", "datumSprejetja"):
        d = item.get(field) or ""
        if re.match(r"\d{4}-\d{2}-\d{2}", d):
            return d
    sop = item.get("sop", "")
    m   = re.match(r"(\d{4})-", sop)
    return f"{m.group(1)}-07-01" if m else "2000-07-01"


def make_frontmatter(item):
    def esc(s):
        return (s or "").replace('"', '\\"')
    zid    = item.get("zunanjiId", "")
    sop    = item.get("sop", "")
    prefix = "".join(c for c in zid if c.isalpha())
    vrsta  = VRSTA_MAP.get(prefix, prefix.lower())
    return (
        "---\n"
        f"kratica: {zid}\n"
        f'naziv: "{esc(item.get("nazivAkta"))}"\n'
        f'vrsta: "{vrsta}"\n'
        f"datum: {item_date(item)}\n"
        f"sop: {sop}\n"
        f'organ: "{esc(item.get("organSprejemaAliIzdaje"))}"\n'
        f'status: "{esc((item.get("semafor") or {}).get("naziv"))}"\n'
        f'vir: "{UL_BASE.format(sop=sop)}"\n'
        "---\n"
    )


def git_commit_item(filepath, date_str, message):
    e   = os.environ.copy()
    iso = f"{date_str}T12:00:00+01:00"
    e["GIT_AUTHOR_DATE"]    = iso
    e["GIT_COMMITTER_DATE"] = iso
    subprocess.run(["git", "add", str(filepath)], cwd=str(REPO_DIR), check=True)
    subprocess.run(
        ["git", "commit", "-m", message, "--allow-empty-message"],
        cwd=str(REPO_DIR), env=e, check=True, capture_output=True,
    )


# ── Progress ───────────────────────────────────────────────────────────────────

def load_progress():
    if PROGRESS_FILE.exists():
        return set(json.loads(PROGRESS_FILE.read_text()))
    return set()


def save_progress(done):
    PROGRESS_FILE.write_text(json.dumps(list(done)))


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="TRUBAR podzakonski fetcher")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit",   type=int,   default=0,
                        help="Max items to process (0=all)")
    parser.add_argument("--delay",   type=float, default=0.5,
                        help="Seconds between Uradni list requests")
    parser.add_argument("--from-year", type=int, default=0,
                        help="Skip years before this")
    args = parser.parse_args()

    LAW_DIR.mkdir(exist_ok=True)
    done = load_progress()

    print("Fetching year list from PISRS...")
    years = pisrs_years()
    print(f"Found {len(years)} years: {years[0][0]}–{years[-1][0]}")

    if args.from_year:
        years = [(y, c) for y, c in years if y >= args.from_year]

    # Collect all wanted items year by year
    all_items = []
    seen_zids = set()
    for year, count in years:
        batch = []
        for item in pisrs_items_for_year(year):
            zid = item.get("zunanjiId", "")
            if wanted(item) and zid not in seen_zids:
                batch.append(item)
                seen_zids.add(zid)
        if batch:
            print(f"  {year}: {len(batch)} podzakonski (of {count} total)")
            all_items.extend(batch)

    print(f"\nTotal: {len(all_items)} podzakonski akti to process")
    all_items.sort(key=item_date)

    if args.limit:
        all_items = all_items[:args.limit]

    ok = skip = fail = 0

    for i, item in enumerate(all_items, 1):
        zid   = item.get("zunanjiId", "")
        sop   = item.get("sop", "")
        naziv = item.get("nazivAkta", "")

        if zid in done:
            skip += 1
            continue

        if not sop:
            fail += 1
            done.add(zid)
            save_progress(done)
            continue

        print(f"[{i}/{len(all_items)}] {zid} ({sop})", end=" ", flush=True)

        html = fetch_ul_html(sop)
        if not html:
            print("→ NOT FOUND")
            fail += 1
            done.add(zid)
            save_progress(done)
            continue

        body = html_to_markdown(html)
        if not body:
            print("→ NO TEXT")
            fail += 1
            done.add(zid)
            save_progress(done)
            continue

        filepath = LAW_DIR / item_filename(item)
        content  = make_frontmatter(item) + "\n" + f"# {naziv}\n\n" + body + "\n"
        filepath.write_text(content, encoding="utf-8")

        if not args.dry_run:
            try:
                git_commit_item(filepath, item_date(item), f"[{zid}] {naziv}")
            except subprocess.CalledProcessError as e:
                print(f"→ GIT ERR: {e}")
                fail += 1
                continue

        print("→ OK")
        ok += 1
        done.add(zid)
        save_progress(done)
        time.sleep(args.delay)

    print(f"\nDone: {ok} ok, {skip} skipped, {fail} failed")


if __name__ == "__main__":
    main()
