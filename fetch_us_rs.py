#!/usr/bin/env python3
"""
T.R.U.B.A.R. — Constitutional Court (Ustavno sodišče RS) fetcher

Fetches all ~25,785 decisions from us-rs.si using the JSON listing API,
then scrapes each decision page for metadata + full text.

Files go into us_rs/ directory. NO git commits — run a separate commit
step after the main overnight fetch completes.

Usage:
  python fetch_us_rs.py [--workers 8] [--delay 0.0] [--limit 100]
"""

import json, re, os, time, argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import threading

import requests
from bs4 import BeautifulSoup

import sys
sys.path.insert(0, str(Path(__file__).parent))
from fetch import REPO_DIR

US_RS_BASE    = "https://www.us-rs.si"
LIST_URL      = US_RS_BASE + "/sl/zadeve-in-odlocitve/odlocitve?format=json&page={page}"
PROGRESS_FILE = REPO_DIR / ".progress_us_rs.txt"
OUT_DIR       = REPO_DIR / "us_rs"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "sl-SI,sl;q=0.9",
}
JSON_HEADERS = {**HEADERS, "Accept": "application/json"}

_SAFE_RE = re.compile(r"[^a-zA-Z0-9_-]")
_local   = threading.local()


def _session():
    if not hasattr(_local, "s"):
        s = requests.Session()
        s.headers.update(HEADERS)
        _local.s = s
    return _local.s


# ── Index ─────────────────────────────────────────────────────────────────────

def fetch_all_urls(max_pages=300):
    """Fetch all decision URLs from the JSON API."""
    index_file = REPO_DIR / ".index_us_rs.json"
    if index_file.exists():
        urls = json.loads(index_file.read_text())
        print(f"Loaded {len(urls)} decision URLs from cache.")
        return urls

    print("Building decision index from us-rs.si JSON API...")
    s = requests.Session()
    s.headers.update(JSON_HEADERS)
    urls = []
    for page in range(1, max_pages + 1):
        for attempt in range(4):
            try:
                r = s.get(LIST_URL.format(page=page), timeout=15)
                r.raise_for_status()
                decisions = r.json().get("decisions", [])
                break
            except Exception as e:
                if attempt == 3:
                    print(f"  page {page} failed: {e}")
                    decisions = []
                time.sleep(2 ** attempt)
        if not decisions:
            print(f"  page {page}: empty — done at {len(urls)} total")
            break
        urls.extend(d["url"] for d in decisions if d.get("url"))
        if page % 50 == 0:
            print(f"  page {page}: {len(urls)} so far")
        time.sleep(0.05)

    index_file.write_text(json.dumps(urls))
    print(f"Cached {len(urls)} decision URLs.")
    return urls


# ── Scraper ───────────────────────────────────────────────────────────────────

def _field(soup, label):
    """Find a metadata field by its label text."""
    for dt in soup.find_all(["dt", "th", "label", "strong"]):
        if label.lower() in dt.get_text().lower():
            dd = dt.find_next_sibling()
            if dd:
                return dd.get_text(separator=" ", strip=True)
    # Also try definition lists
    for div in soup.find_all("div"):
        t = div.get_text(strip=True)
        if t.lower().startswith(label.lower()):
            return t[len(label):].strip(" :")
    return ""


def fetch_decision(url):
    """Fetch a single decision page. Returns (slug, metadata_dict, text) or None."""
    for attempt in range(4):
        try:
            r = _session().get(url, timeout=20)
            if r.status_code == 404:
                return None
            r.raise_for_status()
            break
        except Exception as e:
            if attempt == 3:
                return None
            time.sleep(2 ** attempt)

    soup = BeautifulSoup(r.text, "lxml")
    main = soup.find("main") or soup.find(id="main") or soup.find("body")
    if not main:
        return None

    # Extract structured metadata fields
    def find_field(*labels):
        for label in labels:
            # Look for dt/dd pairs or labeled divs
            for tag in main.find_all(["dt", "th"]):
                if label.lower() in tag.get_text().lower():
                    nxt = tag.find_next_sibling(["dd", "td"])
                    if nxt:
                        return nxt.get_text(separator=" ", strip=True)
            # Look in labeled paragraphs / divs
            for tag in main.find_all(["div", "p", "span"],
                                     class_=lambda c: c and label.lower().replace(" ", "-") in c.lower()):
                return tag.get_text(separator=" ", strip=True)
        return ""

    text_full = main.get_text(separator="\n", strip=True)

    # Pull slug from URL: /odlocitve/u-i-2226 → u-i-2226
    slug = url.rstrip("/").split("/")[-1]

    # Extract key metadata from text (it's consistently formatted)
    meta = {}
    lines = [l.strip() for l in text_full.split("\n") if l.strip()]
    for i, line in enumerate(lines):
        low = line.lower()
        if low.startswith("opravilna") and i + 1 < len(lines):
            meta["opravilna_st"] = lines[i + 1]
        elif low.startswith("datum odločitve") and i + 1 < len(lines):
            meta["datum"] = lines[i + 1]
        elif low.startswith("ecli") and i + 1 < len(lines):
            meta["ecli"] = lines[i + 1]
        elif low.startswith("akt:") or low == "akt" and i + 1 < len(lines):
            meta["akt"] = lines[i + 1]
        elif low.startswith("vrsta zadeve") and i + 1 < len(lines):
            meta["vrsta_zadeve"] = lines[i + 1]
        elif low.startswith("vrsta odločitve") and i + 1 < len(lines):
            meta["vrsta_odlocitve"] = lines[i + 1]
        elif low.startswith("vrsta rešitve") and i + 1 < len(lines):
            meta["vrsta_resitve"] = lines[i + 1]
        elif low.startswith("vlagatelj") and i + 1 < len(lines):
            meta["vlagatelj"] = lines[i + 1]
        elif low.startswith("izrek") and i + 1 < len(lines):
            meta["izrek"] = lines[i + 1]
        elif low.startswith("evidenčni stavek") and i + 1 < len(lines):
            meta["evidencni_stavek"] = lines[i + 1]

    return slug, meta, text_full


# ── Progress ──────────────────────────────────────────────────────────────────

_prog_lock = threading.Lock()


def load_progress():
    return set(PROGRESS_FILE.read_text().splitlines()) if PROGRESS_FILE.exists() else set()


def save_progress(slug):
    with _prog_lock:
        with open(PROGRESS_FILE, "a") as f:
            f.write(slug + "\n")


# ── Writer ────────────────────────────────────────────────────────────────────

def make_content(url, slug, meta, text):
    def esc(s): return (s or "").replace('"', '\\"')
    fm = (
        "---\n"
        f"id: {slug}\n"
        f'opravilna_st: "{esc(meta.get("opravilna_st", ""))}"\n'
        f'datum: "{esc(meta.get("datum", ""))}"\n'
        f'ecli: "{esc(meta.get("ecli", ""))}"\n'
        f'vrsta_zadeve: "{esc(meta.get("vrsta_zadeve", ""))}"\n'
        f'vrsta_odlocitve: "{esc(meta.get("vrsta_odlocitve", ""))}"\n'
        f'vrsta_resitve: "{esc(meta.get("vrsta_resitve", ""))}"\n'
        f'vlagatelj: "{esc(meta.get("vlagatelj", ""))}"\n'
        f'vir: "{url}"\n'
        "zbirka: \"Ustavno sodišče RS\"\n"
        "---\n"
    )
    title = meta.get("opravilna_st", slug)
    izrek = meta.get("izrek", "")
    evidencni = meta.get("evidencni_stavek", "")
    body = f"# {title}\n\n"
    if izrek:
        body += f"## Izrek\n\n{izrek}\n\n"
    if evidencni:
        body += f"## Evidenčni stavek\n\n{evidencni}\n\n"
    body += f"## Polno besedilo\n\n{text}\n"
    return fm + body


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--delay",   type=float, default=0.0)
    parser.add_argument("--limit",   type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    OUT_DIR.mkdir(exist_ok=True)

    all_urls = fetch_all_urls()
    done     = load_progress()
    pending  = [u for u in all_urls if u.rstrip("/").split("/")[-1] not in done]

    if args.limit:
        pending = pending[:args.limit]

    skipped = len(all_urls) - len(pending) - (len(all_urls) - len(done))
    # recalc properly
    skipped = len(all_urls) - len(pending)
    print(f"\nTotal: {len(all_urls)} | Done: {len(done)} | Pending: {len(pending)}")
    print(f"Workers: {args.workers}")

    ok = fail = 0
    total = len(pending)

    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(fetch_decision, url): url for url in pending}
        done_n  = 0
        for future in as_completed(futures):
            url   = futures[future]
            slug  = url.rstrip("/").split("/")[-1]
            done_n += 1
            try:
                result = future.result()
            except Exception as e:
                print(f"[{done_n}/{total}] {slug} → EXCEPTION: {e}")
                fail += 1
                save_progress(slug)
                continue

            if result is None:
                print(f"[{done_n}/{total}] {slug} → NO TEXT")
                fail += 1
            else:
                _, meta, text = result
                content  = make_content(url, slug, meta, text)
                filepath = OUT_DIR / f"{_SAFE_RE.sub('_', slug)}.md"
                if not args.dry_run:
                    filepath.write_text(content, encoding="utf-8")
                print(f"[{done_n}/{total}] {slug} → OK ({meta.get('datum', '?')})")
                ok += 1

            save_progress(slug)
            if args.delay:
                time.sleep(args.delay)

    print(f"\nDone: {ok} ok, {fail} failed. Files in {OUT_DIR}/")


if __name__ == "__main__":
    main()
