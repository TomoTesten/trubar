#!/usr/bin/env python3
"""
T.R.U.B.A.R. — general PISRS collection fetcher

Fetches any named PISRS collection year-by-year, downloads text from
Uradni list RS (or PISRS NPB as fallback), and commits to git.

Usage:
  python fetch_pisrs.py --zbirka "Veljavni akti lokalnih skupnosti" [--delay 0.3]
  python fetch_pisrs.py --zbirka "Drugi splošni in posamični akti"
  python fetch_pisrs.py --zbirka "Splošni akti za izvrševanje javnih pooblastil"

Items are stored in si/{safe_zunanjiId}.md  (same directory as other predpisi).
Progress is tracked per-collection in .progress_{safe_name}.json.
"""

import json, re, os, time, argparse, subprocess
from datetime import date
from pathlib import Path

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


# ── PISRS API helpers ──────────────────────────────────────────────────────────

def pisrs_post(params, body, retries=5):
    for attempt in range(retries):
        try:
            r = requests.post(PISRS_FILTER, headers=PISRS_HEADERS,
                              params=params, json=body, timeout=30)
            r.raise_for_status()
            return r.json().get("data") or {}
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    return {}


def pisrs_get(url, retries=4):
    for attempt in range(retries):
        try:
            r = requests.get(url, headers={"User-Agent": PISRS_HEADERS["User-Agent"]}, timeout=20)
            if r.status_code == 200:
                return r.json().get("data")
            if r.status_code == 404:
                return None
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    return None


def pisrs_years(zbirka):
    data = pisrs_post({"cursorMark": "*"}, {"nazivZbirke": [zbirka]})
    return [(f["value"], f["count"])
            for f in data.get("letoObjaveFacet", [])
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
        time.sleep(0.08)


# ── NPB fallback ───────────────────────────────────────────────────────────────

def html_blocks_to_markdown(blocks):
    def strip(html):
        return BeautifulSoup(html or "", "lxml").get_text(separator=" ", strip=True)
    HEADS = {"naslov": "##", "clen": "###", "tocka": "####", "podnaslov": "###",
             "naslovDela": "##", "naslovPoglavja": "##"}
    lines = []
    for b in blocks:
        s, txt = b.get("struktura", ""), strip(b.get("vsebina", ""))
        if not txt:
            continue
        if s in HEADS:
            lines.append(f"\n{HEADS[s]} {txt}\n")
        elif s == "alineja":
            lines.append(f"- {txt}")
        elif s == "opozorilo":
            lines.append(f"> {txt}")
        else:
            lines.append(txt)
    return "\n".join(lines).strip()


def fetch_pisrs_npb(zunanji_id):
    """Try to get consolidated text from PISRS NPB endpoint."""
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

def fetch_sodna_praksa(zunanji_id):
    """Fetch court decision text from sodnapraksa.si."""
    m = re.match(r"doc_(\d+)$", zunanji_id)
    if not m:
        return None
    doc_id = m.group(1)
    url = SODNAPRAKSA_URL.format(id=doc_id)
    for attempt in range(3):
        try:
            r = requests.get(url, headers={"User-Agent": PISRS_HEADERS["User-Agent"]},
                             timeout=20)
            if r.status_code != 200:
                return None
            soup = BeautifulSoup(r.text, "lxml")
            for tag in soup.find_all(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            container = soup.find(id="container") or soup.find("body") or soup
            lines = [l.strip() for l in container.get_text(separator="\n").split("\n")
                     if len(l.strip()) > 40]
            # Drop common navigation lines
            skip = {"Priljubljeni dokumenti", "Nastavitve", "Pomoč", "Iskalnik sodne prakse"}
            lines = [l for l in lines if l not in skip]
            return "\n\n".join(lines) if len(lines) > 3 else None
        except Exception:
            if attempt == 2:
                return None
            time.sleep(2 ** attempt)
    return None


# ── File helpers ───────────────────────────────────────────────────────────────

def safe_name(s):
    return re.sub(r"[^a-zA-Z0-9_-]", "_", s)


def item_date(item):
    for f in ("datumObjave", "datumSprejetja"):
        d = item.get(f) or ""
        if re.match(r"\d{4}-\d{2}-\d{2}", d):
            return d
    sop = item.get("sop") or ""
    m   = re.match(r"(\d{4})-", sop)
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


def git_commit_item(filepath, date_str, message):
    e   = os.environ.copy()
    iso = f"{date_str}T12:00:00+01:00"
    e["GIT_AUTHOR_DATE"]    = iso
    e["GIT_COMMITTER_DATE"] = iso
    subprocess.run(["git", "add", str(filepath)], cwd=str(REPO_DIR), check=True)
    subprocess.run(["git", "commit", "-m", message, "--allow-empty-message"],
                   cwd=str(REPO_DIR), env=e, check=True, capture_output=True)


# ── Progress ───────────────────────────────────────────────────────────────────

def progress_file(zbirka):
    return REPO_DIR / f".progress_{safe_name(zbirka)[:40]}.json"


def load_progress(zbirka):
    pf = progress_file(zbirka)
    return set(json.loads(pf.read_text())) if pf.exists() else set()


def save_progress(zbirka, done):
    progress_file(zbirka).write_text(json.dumps(list(done)))


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
    if not years:
        print("No years found.")
        return []
    print(f"  {len(years)} years: {years[0][0]}–{years[-1][0]}")

    items, seen = [], set()
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

    cf.write_text(json.dumps(items))
    print(f"Cached {len(items)} items.")
    return items


# ── Main ───────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--zbirka",   required=True, help="PISRS collection name")
    parser.add_argument("--dry-run",  action="store_true")
    parser.add_argument("--limit",    type=int,   default=0)
    parser.add_argument("--delay",    type=float, default=0.4)
    parser.add_argument("--no-ul-fallback-npb", action="store_true",
                        help="Skip PISRS NPB fallback if UL fetch fails")
    args = parser.parse_args()

    LAW_DIR.mkdir(exist_ok=True)
    done  = load_progress(args.zbirka)
    items = build_index(args.zbirka)
    items.sort(key=item_date)

    if args.limit:
        items = items[:args.limit]

    print(f"\nProcessing {len(items)} items from '{args.zbirka}'")
    ok = skip = fail = 0

    for i, item in enumerate(items, 1):
        zid   = item.get("zunanjiId", "")
        sop   = item.get("sop") or ""
        naziv = item.get("nazivAkta", "")

        if not zid:
            continue
        if zid in done:
            skip += 1
            continue

        print(f"[{i}/{len(items)}] {zid} ({sop})", end=" ", flush=True)

        body = None

        # Court decisions: fetch from sodnapraksa.si directly
        if zid.startswith("doc_"):
            body = fetch_sodna_praksa(zid)
            if body:
                print("[SP]", end=" ", flush=True)
        else:
            # Try Uradni list first
            if sop:
                html = fetch_ul_html(sop)
                if html:
                    body = html_to_markdown(html)

            # Fallback: PISRS NPB
            if not body and not args.no_ul_fallback_npb:
                body = fetch_pisrs_npb(zid)
                if body:
                    print("[NPB]", end=" ", flush=True)

        if not body:
            print("→ NO TEXT")
            fail += 1
            done.add(zid)
            save_progress(args.zbirka, done)
            continue

        filepath = LAW_DIR / f"{safe_name(zid)}.md"
        content  = make_frontmatter(item) + f"\n# {naziv}\n\n{body}\n"
        filepath.write_text(content, encoding="utf-8")

        if not args.dry_run:
            try:
                git_commit_item(filepath, item_date(item), f"[{zid}] {naziv}")
            except subprocess.CalledProcessError:
                print("→ GIT ERR")
                fail += 1
                continue

        print("→ OK")
        ok += 1
        done.add(zid)
        save_progress(args.zbirka, done)
        time.sleep(args.delay)

    print(f"\nDone: {ok} ok, {skip} skipped, {fail} no-text")


if __name__ == "__main__":
    main()
