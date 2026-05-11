#!/usr/bin/env python3
"""
T.R.U.B.A.R. — Transparentni Register Urejenih Besedil Aktov Republike Slovenije
https://github.com/trubar-si/trubar

Fetches Slovenian law texts from Uradni list RS, converts to Markdown,
and commits each law chronologically so every reform is a commit.

Sources:
  - DZ SZ.XML: list of laws passed by National Assembly (Državni zbor)
  - Uradni list RS: full law text per publication (SOP reference)

Usage:
  python fetch.py [--limit N] [--offset N] [--dry-run]
"""

import xml.etree.ElementTree as ET
import requests
import re
import os
import sys
import time
import json
import argparse
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup

REPO_DIR = Path(__file__).parent
SZ_XML = REPO_DIR / "data" / "SZ_fixed.XML"
SZ_XML_URL = "https://fotogalerija.dz-rs.si/datoteke/opendata/SZ.XML"
PROGRESS_FILE = REPO_DIR / ".progress.json"
LAW_DIR = REPO_DIR / "si"

UL_BASE = "https://www.uradni-list.si/1/objava.jsp?sop={sop}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "sl,en-US;q=0.7,en;q=0.3",
}

ESEGMENT_MAP = {
    "esegment_t": "##",   # Title / naslov zakona
    "esegment_h1": "#",
    "esegment_h2": "##",
    "esegment_h3": "###",
    "esegment_h4": "###",
    "esegment_h5": "####",
    "esegment_h6": "####",
}


def download_sz_xml():
    """Download the DZ SZ.XML if not already present."""
    SZ_XML.parent.mkdir(parents=True, exist_ok=True)
    if SZ_XML.exists():
        print(f"SZ.XML already present ({SZ_XML.stat().st_size // 1024 // 1024} MB)")
        return
    print("Downloading SZ.XML from Državni zbor...")
    resp = requests.get(SZ_XML_URL, stream=True, timeout=120)
    resp.raise_for_status()
    with open(SZ_XML, "wb") as f:
        for chunk in resp.iter_content(chunk_size=65536):
            f.write(chunk)
    print(f"Downloaded {SZ_XML.stat().st_size // 1024 // 1024} MB")


def parse_sz_xml():
    """Parse DZ SZ.XML, return list of law metadata sorted by date.

    Structure: PREDPIS > KARTICA_PREDPISA > KARTICA_* fields.
    """
    tree = ET.parse(str(SZ_XML))
    root = tree.getroot()

    laws = []
    for predpis in root:
        if predpis.tag != "PREDPIS":
            continue
        card = predpis.find("KARTICA_PREDPISA")
        if card is None:
            continue

        def ftext(tag):
            child = card.find(tag)
            return (child.text or "").strip() if child is not None else ""

        sop = ftext("KARTICA_SOP")
        datum = ftext("KARTICA_DATUM")
        if not sop or not datum:
            continue

        kw = [k.text.strip() for k in card.findall("KARTICA_KLJUCNE_BESEDE") if k.text]

        laws.append({
            "sop": sop,
            "kratica": ftext("KARTICA_KRATICA"),
            "naziv": ftext("KARTICA_NAZIV"),
            "datum": datum,
            "vrsta": ftext("KARTICA_VRSTA"),
            "objava": ftext("KARTICA_OBJAVA"),
            "kljucne_besede": kw,
            "unid": ftext("UNID"),
        })

    laws.sort(key=lambda x: x["datum"])
    print(f"Parsed {len(laws)} laws from SZ.XML")
    return laws


def fetch_ul_html(sop, retries=3):
    """Fetch law HTML from Uradni list for given SOP."""
    url = UL_BASE.format(sop=sop)
    for attempt in range(retries):
        try:
            resp = requests.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp.text
            if resp.status_code == 404:
                return None
        except requests.RequestException as e:
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None


def html_to_markdown(html):
    """Convert Uradni list HTML law page to Markdown text."""
    soup = BeautifulSoup(html, "lxml")

    container = soup.find(class_="ul-content-container")
    if not container:
        return None

    lines = []
    seen_title = False

    for tag in container.find_all(True):
        cls_list = tag.get("class") or []
        cls = cls_list[0] if cls_list else ""

        if not cls.startswith("esegment_"):
            continue

        text = tag.get_text(separator="\n", strip=True)
        if not text:
            continue

        if cls in ESEGMENT_MAP:
            heading = ESEGMENT_MAP[cls]
            if cls == "esegment_t" and not seen_title:
                seen_title = True
            lines.append(f"\n{heading} {text}\n")
        elif cls in ("esegment_p", "esegment_p1", "esegment_p2", "esegment_p3"):
            lines.append(f"{text}\n")
        elif cls in ("esegment_c1", "esegment_c2", "esegment_c3"):
            lines.append(f"{text}\n")
        elif cls in ("esegment_li", "esegment_li1", "esegment_li2"):
            lines.append(f"- {text}\n")
        elif cls == "esegment_table":
            lines.append(f"\n{text}\n")
        else:
            lines.append(f"{text}\n")

    return "\n".join(lines).strip()


def make_frontmatter(law):
    """Generate YAML frontmatter for a law."""
    kw_parts = ", ".join(f'"{k}"' for k in law["kljucne_besede"])
    naziv_escaped = law["naziv"].replace('"', '\\"')
    vrsta_escaped = law["vrsta"].replace('"', '\\"')
    objava_escaped = law["objava"].replace('"', '\\"')
    return (
        "---\n"
        f"kratica: {law['kratica']}\n"
        f'naziv: "{naziv_escaped}"\n'
        f'vrsta: "{vrsta_escaped}"\n'
        f"datum: {law['datum']}\n"
        f"sop: {law['sop']}\n"
        f'objava: "{objava_escaped}"\n'
        f"kljucne_besede: [{kw_parts}]\n"
        f'vir: "{UL_BASE.format(sop=law["sop"])}"\n'
        "---\n"
    )


def law_filename(law):
    """Safe filename for a law."""
    kratica = law["kratica"] or law["sop"].replace("-", "_")
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", kratica)
    return f"{safe}.md"


def git_commit(filepath, date_str, message, env=None):
    """Stage and commit a single file with a backdated timestamp."""
    e = os.environ.copy()
    iso = f"{date_str}T12:00:00+01:00"
    e["GIT_AUTHOR_DATE"] = iso
    e["GIT_COMMITTER_DATE"] = iso
    if env:
        e.update(env)

    subprocess.run(["git", "add", str(filepath)], cwd=str(REPO_DIR), check=True)
    subprocess.run(
        ["git", "commit", "-m", message, "--allow-empty-message"],
        cwd=str(REPO_DIR), env=e, check=True,
        capture_output=True,
    )


def load_progress():
    if PROGRESS_FILE.exists():
        return set(json.loads(PROGRESS_FILE.read_text()))
    return set()


def save_progress(done):
    PROGRESS_FILE.write_text(json.dumps(list(done)))


def main():
    parser = argparse.ArgumentParser(description="legalize-si fetcher")
    parser.add_argument("--limit", type=int, default=0, help="Max laws to process (0=all)")
    parser.add_argument("--offset", type=int, default=0, help="Skip first N laws")
    parser.add_argument("--dry-run", action="store_true", help="Fetch but don't commit")
    parser.add_argument("--delay", type=float, default=0.5, help="Seconds between requests")
    parser.add_argument("--no-download", action="store_true", help="Skip SZ.XML download check")
    args = parser.parse_args()

    if not args.no_download:
        download_sz_xml()

    LAW_DIR.mkdir(exist_ok=True)

    laws = parse_sz_xml()
    done = load_progress()

    if args.offset:
        laws = laws[args.offset:]
    if args.limit:
        laws = laws[:args.limit]

    ok = skip = fail = 0

    for i, law in enumerate(laws, 1):
        sop = law["sop"]

        if sop in done:
            skip += 1
            continue

        kratica = law["kratica"] or sop
        print(f"[{i}/{len(laws)}] {kratica} ({sop}) - {law['datum']}", end=" ", flush=True)

        html = fetch_ul_html(sop)
        if not html:
            print("→ NOT FOUND")
            fail += 1
            done.add(sop)
            save_progress(done)
            continue

        body = html_to_markdown(html)
        if not body:
            print("→ NO TEXT")
            fail += 1
            done.add(sop)
            save_progress(done)
            continue

        filename = law_filename(law)
        filepath = LAW_DIR / filename
        content = make_frontmatter(law) + "\n" + f"# {law['naziv']}\n\n" + body + "\n"
        filepath.write_text(content, encoding="utf-8")

        if not args.dry_run:
            msg = f"[{kratica}] {law['naziv']}"
            try:
                git_commit(filepath, law["datum"], msg)
            except subprocess.CalledProcessError as e:
                print(f"→ GIT ERR: {e}")
                fail += 1
                continue

        print("→ OK")
        ok += 1
        done.add(sop)
        save_progress(done)

        time.sleep(args.delay)

    print(f"\nDone: {ok} ok, {skip} skipped, {fail} failed")


if __name__ == "__main__":
    main()
