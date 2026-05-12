#!/usr/bin/env python3
"""
Build a kratica → court decisions index from local parquet cache.
Output: data/court_links.json  {kratica: [{id, vir, zbirka, datum},...]}
Capped at 20 most recent decisions per kratica.
"""
import json, re
from collections import Counter, defaultdict
from pathlib import Path

import pyarrow.parquet as pq
import yaml

REPO_DIR    = Path(__file__).parent
CACHE_DIR   = REPO_DIR / ".court_hf_cache"
SI_DIR      = REPO_DIR / "si"
OUTPUT      = REPO_DIR / "data" / "court_links.json"
MAX_PER_KEY = 20

# Tokeniser: extract word-like tokens from text (fast, single-pass)
_TOK_RE = re.compile(r'[A-ZČŠŽ][A-Za-zÀ-žčšž0-9-]{1,}')


def load_kratice():
    kratice = set()
    for p in SI_DIR.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="replace")
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            front = yaml.safe_load(parts[1]) or {}
        except Exception:
            continue
        k = front.get("kratica")
        if k and len(k) >= 2:
            kratice.add(k)
    return kratice


def find_kratice_in_text(text, kratice_set):
    """O(len(text)) lookup: tokenise then count. Requires ≥2 occurrences to reduce false positives."""
    counts = Counter(_TOK_RE.findall(text))
    return {k for k, c in counts.items() if c >= 2 and k in kratice_set}


def main():
    print("Loading kratice from si/...")
    kratice = load_kratice()
    print(f"  {len(kratice)} kratice")

    index = defaultdict(list)  # kratica → [{id, vir, zbirka, datum}]

    parquets = sorted(CACHE_DIR.glob("*.parquet"))
    print(f"Scanning {len(parquets)} parquet shards...")

    for i, pf in enumerate(parquets):
        schema = pq.read_schema(pf)
        field_names = {f.name for f in schema}
        is_us = "opravilna_st" in field_names  # Constitutional Court schema
        cols = ["id", "vir", "datum", "text"] + (["opravilna_st"] if is_us else ["zbirka"])
        tbl = pq.read_table(pf, columns=cols)
        rows = tbl.to_pydict()
        n = len(rows["id"])
        for j in range(n):
            text = rows["text"][j] or ""
            if not text:
                continue
            found = find_kratice_in_text(text, kratice)
            if not found:
                continue
            if is_us:
                zbirka = "Ustavno sodišče RS"
            else:
                zbirka = rows["zbirka"][j] or ""
            entry = {
                "id":     rows["id"][j] or "",
                "vir":    rows["vir"][j] or "",
                "zbirka": zbirka,
                "datum":  rows["datum"][j] or "",
            }
            for k in found:
                index[k].append(entry)
        if (i + 1) % 5 == 0:
            print(f"  [{i+1}/{len(parquets)}] {sum(len(v) for v in index.values()):,} links so far", flush=True)

    print("Sorting and capping per kratica...")
    result = {}
    for k, entries in index.items():
        entries.sort(key=lambda e: e["datum"], reverse=True)
        result[k] = entries[:MAX_PER_KEY]

    print(f"  {len(result)} kratice with links, {sum(len(v) for v in result.values()):,} total")

    OUTPUT.parent.mkdir(exist_ok=True)
    OUTPUT.write_text(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    size = OUTPUT.stat().st_size
    print(f"Written {OUTPUT} ({size/1024:.0f} KB)")


if __name__ == "__main__":
    main()
