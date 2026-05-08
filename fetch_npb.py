#!/usr/bin/env python3
"""
T.R.U.B.A.R. — fetch NPB (Neuradno Prečiščeno Besedilo / consolidated texts)

For each predpis in the PISRS index, fetches the currently-active consolidated
text via two undocumented but public PISRS API endpoints:

  GET /api/rezultat/zbirka/id/{zunanjiId}           → NPB version list
  GET /api/rezultat/neuradno-precisceno-besedilo/{id}/details → full text blocks

Stores results in si/npb/{zunanjiId}.md with YAML frontmatter.

Usage:
  python fetch_npb.py [--limit N] [--dry-run] [--delay SEC]
"""

import json, re, os, time, argparse, subprocess
from datetime import date
from pathlib import Path

import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch import REPO_DIR

NPB_DIR        = REPO_DIR / "si" / "npb"
PROGRESS_FILE  = REPO_DIR / ".progress_npb.json"
INDEX_CACHE    = REPO_DIR / ".pisrs_index_cache.json"

PISRS_BASE     = "https://pisrs.si/api/rezultat"
PISRS_HEADERS  = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0"}

TODAY = date.today().isoformat()

# ── PISRS API ──────────────────────────────────────────────────────────────────

def get_with_retry(url, retries=4):
    for attempt in range(retries):
        try:
            r = requests.get(url, headers=PISRS_HEADERS, timeout=20)
            if r.status_code == 200:
                return r.json().get("data")
            if r.status_code == 404:
                return None
        except Exception as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** (attempt + 1))
    return None


def get_npb_versions(zunanji_id):
    """Return list of NPB version dicts for a predpis, newest-first."""
    data = get_with_retry(f"{PISRS_BASE}/zbirka/id/{zunanji_id}")
    if not data:
        return []
    return (data.get("besedilo") or {}).get("npbVerzije") or []


def pick_current_npb(versions):
    """Return the currently-active NPB version (latest startDate ≤ today, or last one)."""
    if not versions:
        return None
    active = [v for v in versions
              if not v.get("datumZacetkaUporabe") or v["datumZacetkaUporabe"] <= TODAY]
    return active[-1] if active else versions[-1]


def get_npb_text(npb_id):
    """Return list of content blocks for a specific NPB version ID."""
    data = get_with_retry(f"{PISRS_BASE}/neuradno-precisceno-besedilo/{npb_id}/details")
    if not data:
        return []
    return data.get("besedilo") or []


# ── HTML→Markdown ──────────────────────────────────────────────────────────────

def html_to_text(html):
    """Strip HTML tags, return clean text."""
    if not html:
        return ""
    return BeautifulSoup(html, "lxml").get_text(separator=" ", strip=True)


STRUKTURA_MAP = {
    "naslov":          "##",
    "clen":            "###",
    "tocka":           "####",
    "podnaslov":       "###",
    "naslovDela":      "##",
    "naslovOddelka":   "###",
    "naslovRazdelka":  "####",
    "naslovPoglavja":  "##",
    "naslovPododdelka": "####",
}


def blocks_to_markdown(blocks):
    lines = []
    for block in blocks:
        s   = block.get("struktura", "")
        txt = html_to_text(block.get("vsebina", ""))
        if not txt:
            continue

        if s in STRUKTURA_MAP:
            lines.append(f"\n{STRUKTURA_MAP[s]} {txt}\n")
        elif s == "alineja":
            lines.append(f"- {txt}")
        elif s == "opozorilo":
            lines.append(f"> {txt}")
        elif s in ("odstavek", "pravna_podlaga", "uvod", "uvodna_izjava",
                   "zakljucek", "podpis", "datum", ""):
            lines.append(txt)
        else:
            lines.append(txt)

    return "\n".join(lines).strip()


# ── File helpers ───────────────────────────────────────────────────────────────

def make_frontmatter(item, npb_version):
    def esc(s): return (s or "").replace('"', '\\"')
    zid   = item.get("zunanjiId", "")
    naziv = esc(item.get("nazivAkta") or item.get("naziv", ""))
    npb_n = esc(npb_version.get("naziv", ""))
    start = npb_version.get("datumZacetkaUporabe") or item.get("datumObjave") or ""
    sop   = item.get("sop", "")
    return (
        "---\n"
        f"kratica: {zid}\n"
        f'naziv: "{naziv}"\n'
        f"sop: {sop}\n"
        f'npb: "{npb_n}"\n'
        f"veljaOd: {start}\n"
        f'vir: "https://pisrs.si/pregledNpb?id={zid}"\n'
        "---\n"
    )


def git_commit_npb(filepath, date_str, message):
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

def load_all_items():
    """Load items from PISRS index cache (built by fetch_podzakonski.py)."""
    # Also include zakoni from the cache if present, else read from si/ frontmatter
    items = []
    # From podzakonski cache
    if INDEX_CACHE.exists():
        podzakonski = json.loads(INDEX_CACHE.read_text())
        items.extend(podzakonski)
        print(f"Loaded {len(podzakonski)} podzakonski from cache")

    # Add zakoni by reading existing si/*.md frontmatter for zunanjiId
    si_dir = REPO_DIR / "si"
    zids_seen = {item.get("zunanjiId") for item in items}
    zakon_count = 0
    for f in sorted(si_dir.glob("*.md")):
        text = f.read_text(encoding="utf-8")
        m = re.search(r'^kratica:\s*(\S+)', text, re.M)
        if not m:
            continue
        zid = m.group(1)
        if zid in zids_seen:
            continue
        sop_m = re.search(r'^sop:\s*(\S+)', text, re.M)
        naziv_m = re.search(r'^naziv:\s*"(.+)"', text, re.M)
        items.append({
            "zunanjiId": zid,
            "sop": sop_m.group(1) if sop_m else "",
            "nazivAkta": naziv_m.group(1) if naziv_m else zid,
            "datumObjave": "",
        })
        zids_seen.add(zid)
        zakon_count += 1
    print(f"Added {zakon_count} zakoni from si/*.md")
    return items


def main():
    parser = argparse.ArgumentParser(description="TRUBAR NPB fetcher")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit",   type=int,   default=0)
    parser.add_argument("--delay",   type=float, default=0.3)
    args = parser.parse_args()

    NPB_DIR.mkdir(parents=True, exist_ok=True)
    done = load_progress()

    items = load_all_items()
    print(f"Total items: {len(items)}")

    if args.limit:
        items = items[:args.limit]

    ok = skip = no_npb = fail = 0

    for i, item in enumerate(items, 1):
        zid = item.get("zunanjiId", "")
        if not zid:
            continue
        if zid in done:
            skip += 1
            continue

        print(f"[{i}/{len(items)}] {zid}", end=" ", flush=True)

        try:
            versions = get_npb_versions(zid)
        except Exception as e:
            print(f"→ ERR {e}")
            fail += 1
            continue

        if not versions:
            print("→ no NPB")
            no_npb += 1
            done.add(zid)
            save_progress(done)
            continue

        current = pick_current_npb(versions)
        npb_id  = current["id"]
        npb_n   = current.get("naziv", "NPB")

        try:
            blocks = get_npb_text(npb_id)
        except Exception as e:
            print(f"→ ERR text {e}")
            fail += 1
            continue

        if not blocks:
            print(f"→ empty {npb_n}")
            fail += 1
            done.add(zid)
            save_progress(done)
            continue

        body     = blocks_to_markdown(blocks)
        filepath = NPB_DIR / f"{re.sub(r'[^a-zA-Z0-9_-]', '_', zid)}.md"
        naziv    = item.get("nazivAkta") or item.get("naziv", zid)
        content  = make_frontmatter(item, current) + f"\n# {naziv}\n\n{body}\n"
        filepath.write_text(content, encoding="utf-8")

        veljaOd = current.get("datumZacetkaUporabe") or item.get("datumObjave") or TODAY

        if not args.dry_run:
            try:
                git_commit_npb(filepath, veljaOd,
                               f"[{zid}] {npb_n}: {naziv[:80]}")
            except subprocess.CalledProcessError as e:
                print(f"→ GIT ERR")
                fail += 1
                continue

        print(f"→ OK ({npb_n}, {len(blocks)} blocks)")
        ok += 1
        done.add(zid)
        save_progress(done)
        time.sleep(args.delay)

    print(f"\nDone: {ok} ok, {skip} skipped, {no_npb} no-NPB, {fail} failed")


if __name__ == "__main__":
    main()
