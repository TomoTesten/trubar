#!/usr/bin/env python3
"""
build_db.py — Build trubar.db SQLite database from si/*.md and si/npb/*.md.

Tables:
  laws        — one row per law/act (kratica, naziv, vrsta, datum, organ,
                status, sop, vir, body_text, is_npb)
  amendments  — one row per sprememba entry from frontmatter
  laws_fts    — FTS5 virtual table over naziv + body_text

Usage:
  python3 build_db.py [--db PATH]     (default: trubar.db in repo root)
"""

import argparse
import re
import sqlite3
import sys
from pathlib import Path

# ── YAML frontmatter parsing (stdlib only, no PyYAML dependency) ───────────────

def parse_frontmatter(text: str) -> tuple[dict, str]:
    """
    Split a Markdown file into (frontmatter_dict, body_text).

    Frontmatter is delimited by leading '---' lines.
    We do a minimal YAML parse sufficient for this dataset:
      - scalar strings (quoted or unquoted)
      - lists of dicts (the spremembe block)
    Returns ({}, text) if no frontmatter found.
    """
    if not text.startswith("---"):
        return {}, text

    # Find closing '---'
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text

    yaml_block = text[3:end].strip()
    body       = text[end + 4:].lstrip("\n")

    fm = _parse_yaml_block(yaml_block)
    return fm, body


def _parse_yaml_block(block: str) -> dict:
    """Parse the flat-ish YAML frontmatter used in T.R.U.B.A.R. files."""
    result: dict = {}
    lines  = block.splitlines()
    i      = 0
    while i < len(lines):
        line = lines[i]
        # Skip blank / comment lines
        if not line.strip() or line.strip().startswith("#"):
            i += 1
            continue

        # Key: value
        m = re.match(r'^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)', line)
        if not m:
            i += 1
            continue

        key   = m.group(1)
        value = m.group(2).strip()

        # Multi-line list block (spremembe:)
        if value == "" or value == "[]":
            # Peek ahead for list items
            items = []
            j = i + 1
            while j < len(lines) and (lines[j].startswith("  ") or lines[j].startswith("\t")):
                item_line = lines[j]
                # Each item block starts with "  - key: value"
                list_m = re.match(r'\s+-\s+([A-Za-z_][A-Za-z0-9_]*):\s*(.*)', item_line)
                if list_m:
                    items.append({list_m.group(1): _clean_value(list_m.group(2))})
                    # Merge subsequent indented "    key: value" lines into the same dict
                    k = j + 1
                    while k < len(lines) and re.match(r'\s{4,}([A-Za-z_][A-Za-z0-9_]*):\s*(.*)', lines[k]):
                        sub = re.match(r'\s+([A-Za-z_][A-Za-z0-9_]*):\s*(.*)', lines[k])
                        if sub and items:
                            items[-1][sub.group(1)] = _clean_value(sub.group(2))
                        k += 1
                    j = k
                else:
                    # Plain indented sub-key (e.g. "    datum: ...")
                    sub = re.match(r'\s+([A-Za-z_][A-Za-z0-9_]*):\s*(.*)', item_line)
                    if sub and items:
                        items[-1][sub.group(1)] = _clean_value(sub.group(2))
                        j += 1
                    else:
                        j += 1
            if items:
                result[key] = items
                i = j
            else:
                result[key] = value if value else None
                i += 1
        else:
            result[key] = _clean_value(value)
            i += 1

    return result


def _clean_value(v: str) -> str:
    """Strip surrounding quotes and trim whitespace."""
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or \
       (v.startswith("'") and v.endswith("'")):
        v = v[1:-1]
    return v


# ── DB schema ──────────────────────────────────────────────────────────────────

SCHEMA = """
CREATE TABLE IF NOT EXISTS laws (
    id         INTEGER PRIMARY KEY,
    kratica    TEXT NOT NULL,
    naziv      TEXT,
    vrsta      TEXT,
    datum      TEXT,
    organ      TEXT,
    status     TEXT,
    sop        TEXT,
    vir        TEXT,
    body_text  TEXT,
    is_npb     INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS amendments (
    kratica           TEXT,
    sprememba_kratica TEXT,
    sprememba_naziv   TEXT,
    datum             TEXT
);

CREATE VIRTUAL TABLE IF NOT EXISTS laws_fts USING fts5(
    naziv,
    body_text,
    content=laws,
    content_rowid=id,
    tokenize="unicode61"
);
"""

# ── main ───────────────────────────────────────────────────────────────────────

REPO = Path(__file__).parent

BATCH_SIZE   = 500
PRINT_EVERY  = 5000


def iter_md_files():
    """Yield (Path, is_npb) for all si/*.md and si/npb/*.md files."""
    si_dir  = REPO / "si"
    npb_dir = REPO / "si" / "npb"

    for p in sorted(si_dir.glob("*.md")):
        yield p, 0
    if npb_dir.is_dir():
        for p in sorted(npb_dir.glob("*.md")):
            yield p, 1


def build(db_path: Path):
    print(f"Building {db_path} …")

    conn = sqlite3.connect(str(db_path))
    conn.executescript("PRAGMA journal_mode=WAL; PRAGMA synchronous=NORMAL;")
    conn.executescript(SCHEMA)

    # Truncate existing data so a re-run is idempotent
    conn.executescript("""
        DELETE FROM amendments;
        DELETE FROM laws;
        DELETE FROM laws_fts;
    """)

    law_rows       = []   # (kratica, naziv, vrsta, datum, organ, status, sop, vir, body_text, is_npb)
    amendment_rows = []   # (kratica, sprememba_kratica, sprememba_naziv, datum)

    total_files    = 0
    total_inserted = 0

    def flush_laws():
        nonlocal total_inserted
        if not law_rows:
            return
        conn.executemany(
            """INSERT OR REPLACE INTO laws
               (kratica, naziv, vrsta, datum, organ, status, sop, vir, body_text, is_npb)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            law_rows
        )
        total_inserted += len(law_rows)
        law_rows.clear()

    def flush_amendments():
        if not amendment_rows:
            return
        conn.executemany(
            """INSERT INTO amendments
               (kratica, sprememba_kratica, sprememba_naziv, datum)
               VALUES (?, ?, ?, ?)""",
            amendment_rows
        )
        amendment_rows.clear()

    for path, is_npb in iter_md_files():
        total_files += 1
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            print(f"  WARN: cannot read {path}: {e}", file=sys.stderr)
            continue

        fm, body = parse_frontmatter(text)

        kratica = fm.get("kratica") or path.stem
        naziv   = fm.get("naziv")
        vrsta   = fm.get("vrsta")
        datum   = str(fm.get("datum") or fm.get("veljaOd") or "")
        organ   = fm.get("organ")
        status  = fm.get("status")
        sop     = fm.get("sop")
        vir     = fm.get("vir")

        law_rows.append((
            kratica, naziv, vrsta, datum, organ, status, sop, vir,
            body.strip() if body else None,
            is_npb
        ))

        # Collect spremembe
        spremembe = fm.get("spremembe") or []
        if isinstance(spremembe, list):
            for s in spremembe:
                if not isinstance(s, dict):
                    continue
                amendment_rows.append((
                    kratica,
                    s.get("kratica"),
                    s.get("naziv"),
                    str(s.get("datum") or "")
                ))

        if len(law_rows) >= BATCH_SIZE:
            flush_laws()
            flush_amendments()
            conn.commit()

        if total_files % PRINT_EVERY == 0:
            print(f"  … processed {total_files:,} files, inserted {total_inserted:,} laws so far")

    # Final flush
    flush_laws()
    flush_amendments()
    conn.commit()

    # Populate FTS index
    print("Populating FTS5 index …")
    conn.execute("INSERT INTO laws_fts(laws_fts) VALUES('rebuild')")
    conn.commit()

    # Summary
    (n_laws,)  = conn.execute("SELECT COUNT(*) FROM laws").fetchone()
    (n_amend,) = conn.execute("SELECT COUNT(*) FROM amendments").fetchone()
    print(f"Done. {n_laws:,} laws, {n_amend:,} amendment rows → {db_path}")
    conn.close()


def main():
    parser = argparse.ArgumentParser(description="Build trubar.db from si/*.md")
    parser.add_argument("--db", default=str(REPO / "trubar.db"),
                        help="Output SQLite path (default: trubar.db in repo root)")
    args = parser.parse_args()
    build(Path(args.db))


if __name__ == "__main__":
    main()
