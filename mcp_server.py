#!/usr/bin/env python3
"""
T.R.U.B.A.R. MCP server — query Slovenian legislation.

Preferred mode: reads from trubar.db (SQLite, built by build_db.py).
Fallback mode:  file-based parsing from si/*.md (original behaviour).

Tools:
  get_law(kratica)                              — full text of a law by kratica
  get_law_at_date(kratica, date)                — text as it was on a given date
  get_law_on_date(kratica, date)                — which version was in force on date
  search(query, vrsta?, limit?)                 — FTS5 / grep search
  search_laws(query, max_results?)              — alias kept for back-compat
  list_laws(vrsta?, organ?, status?, limit?,    — browse with filters
            offset?)
  get_amendments(kratica)                       — amendment list for a law
  get_law_history(kratica)                      — git commit history
  query_sql(sql)                                — arbitrary read-only SQL (SELECT only)

Usage (stdio transport — works with Claude Desktop / Claude Code):
  python mcp_server.py

Register in Claude Desktop (~/.claude.json or settings):
  {
    "mcpServers": {
      "trubar": {
        "command": "python3",
        "args": ["/data/T.R.U.B.A.R./mcp_server.py"]
      }
    }
  }
"""

import re
import sqlite3
import subprocess
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

REPO    = Path(__file__).parent
SI_DIR  = REPO / "si"
DB_PATH = REPO / "trubar.db"

# ── DB connection (opened once at import time if available) ────────────────────

_db: Optional[sqlite3.Connection] = None

def _get_db() -> Optional[sqlite3.Connection]:
    """Return a read-only DB connection, or None if trubar.db doesn't exist."""
    global _db
    if _db is not None:
        return _db
    if not DB_PATH.exists():
        return None
    try:
        _db = sqlite3.connect(
            f"file:{DB_PATH}?mode=ro",
            uri=True,
            check_same_thread=False,
        )
        _db.row_factory = sqlite3.Row
        return _db
    except Exception:
        return None


def _db_available() -> bool:
    return _get_db() is not None


# ── MCP setup ─────────────────────────────────────────────────────────────────

mcp = FastMCP("trubar", instructions=(
    "Query Slovenian legislation from the T.R.U.B.A.R. repository. "
    "Laws are in si/*.md with YAML frontmatter; trubar.db provides fast FTS5 search. "
    "Git history tracks every amendment chronologically."
))


# ── legacy file-based helpers (fallback) ──────────────────────────────────────

def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=str(REPO),
                       capture_output=True, text=True, check=check)
    return r.stdout.strip()


def find_file(kratica: str) -> Optional[Path]:
    """Find si/{kratica}.md (case-insensitive)."""
    p = SI_DIR / f"{kratica}.md"
    if p.exists():
        return p
    pattern = kratica.upper()
    for f in SI_DIR.glob("*.md"):
        if f.stem.upper() == pattern:
            return f
    return None


def sop_to_path(sop: str) -> Optional[Path]:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", sop)
    p    = SI_DIR / f"{safe}.md"
    return p if p.exists() else None


# ── tools ─────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_law(kratica: str) -> str:
    """
    Return the current full text of a law or act.

    kratica: the abbreviation (e.g. 'ZKP', 'URED4488') or SOP reference.
    When trubar.db is available, returns frontmatter fields + body_text from the DB.
    Falls back to reading si/{kratica}.md directly.
    """
    db = _get_db()
    if db:
        row = db.execute(
            "SELECT * FROM laws WHERE kratica = ? COLLATE NOCASE LIMIT 1",
            (kratica,)
        ).fetchone()
        if row:
            lines = [
                f"kratica: {row['kratica']}",
                f"naziv: {row['naziv']}",
                f"vrsta: {row['vrsta']}",
                f"datum: {row['datum']}",
                f"organ: {row['organ']}",
                f"status: {row['status']}",
                f"sop: {row['sop']}",
                f"vir: {row['vir']}",
                f"is_npb: {row['is_npb']}",
                "",
                row["body_text"] or "",
            ]
            return "\n".join(lines)
        # not in DB — fall through to file

    path = find_file(kratica) or sop_to_path(kratica)
    if path is None:
        return f"No file or DB entry found for '{kratica}'. Try list_laws() to browse."
    return path.read_text(encoding="utf-8")


@mcp.tool()
def get_law_at_date(kratica: str, date: str) -> str:
    """
    Return the text of a law as it was on a specific date (via git history).

    kratica: abbreviation (e.g. 'ZKP')
    date:    ISO date string, e.g. '2015-01-01'
    """
    path = find_file(kratica) or sop_to_path(kratica)
    if path is None:
        return f"No file found for '{kratica}'."
    rel = path.relative_to(REPO)
    try:
        commit = git("rev-list", "-1", f"--before={date}", "HEAD", "--", str(rel))
        if not commit:
            return f"No commits for {kratica} before {date}."
        return git("show", f"{commit}:{rel}")
    except subprocess.CalledProcessError as e:
        return f"git error: {e.stderr}"


@mcp.tool()
def get_law_on_date(kratica: str, date: str) -> str:
    """
    Determine which version of a law was in force on a given date.

    Returns the law's datum (enactment date) and lists which amendments had
    already been applied (amendment datum <= given date).

    kratica: abbreviation, e.g. 'ZKP'
    date:    ISO date string, e.g. '2020-01-01'
    """
    db = _get_db()

    # Fetch base law datum
    base_datum = None
    base_naziv = None
    if db:
        row = db.execute(
            "SELECT kratica, naziv, datum FROM laws WHERE kratica = ? COLLATE NOCASE LIMIT 1",
            (kratica,)
        ).fetchone()
        if row:
            base_datum = row["datum"]
            base_naziv = row["naziv"]
    else:
        path = find_file(kratica)
        if path:
            text = path.read_text(encoding="utf-8")
            m = re.search(r'^datum:\s*(.+)$', text, re.M)
            if m:
                base_datum = m.group(1).strip()
            m2 = re.search(r'^naziv:\s*"(.+)"', text, re.M)
            if m2:
                base_naziv = m2.group(1)

    if not base_datum:
        return f"No law found for '{kratica}'."

    if base_datum > date:
        return (
            f"Law '{kratica}' ({base_naziv}) was enacted on {base_datum}, "
            f"after the requested date {date}. It was not in force then."
        )

    # Fetch amendments that predate `date`
    amendments_before = []
    amendments_after  = []
    if db:
        rows = db.execute(
            "SELECT sprememba_kratica, sprememba_naziv, datum FROM amendments "
            "WHERE kratica = ? COLLATE NOCASE ORDER BY datum",
            (kratica,)
        ).fetchall()
        for r in rows:
            if r["datum"] and r["datum"] <= date:
                amendments_before.append(r)
            else:
                amendments_after.append(r)
    else:
        path = find_file(kratica)
        if path:
            text = path.read_text(encoding="utf-8")
            # crude parse of spremembe block
            for m in re.finditer(
                r'- kratica:\s*(\S+).*?datum:\s*(\S+).*?naziv:\s*"([^"]+)"',
                text, re.S
            ):
                sk, sd, sn = m.group(1), m.group(2), m.group(3)
                entry = {"sprememba_kratica": sk, "datum": sd, "sprememba_naziv": sn}
                if sd <= date:
                    amendments_before.append(entry)
                else:
                    amendments_after.append(entry)

    def fmt(r):
        k = r["sprememba_kratica"] if isinstance(r, sqlite3.Row) else r["sprememba_kratica"]
        d = r["datum"]             if isinstance(r, sqlite3.Row) else r["datum"]
        n = r["sprememba_naziv"]   if isinstance(r, sqlite3.Row) else r["sprememba_naziv"]
        return f"  {k} ({d}): {n}"

    lines = [
        f"Law '{kratica}' — {base_naziv}",
        f"Base enactment: {base_datum}",
        f"Query date:     {date}",
        "",
    ]
    if amendments_before:
        lines.append(f"Amendments in force by {date} ({len(amendments_before)}):")
        lines += [fmt(r) for r in amendments_before]
    else:
        lines.append("No amendments in force by this date.")

    if amendments_after:
        lines.append(f"\nLater amendments (not yet in force on {date}):")
        lines += [fmt(r) for r in amendments_after]

    return "\n".join(lines)


@mcp.tool()
def search(query: str, vrsta: str = "", limit: int = 20) -> str:
    """
    Full-text search across all law texts.

    Uses FTS5 (trubar.db) when available; falls back to grep over si/*.md.

    query: search term or FTS5 expression (e.g. 'osebni podatki', 'kazen*')
    vrsta: optional filter by law type ('zakon', 'uredba', 'pravilnik', …)
    limit: maximum results returned (default 20)
    """
    db = _get_db()
    if db:
        vrsta_param = vrsta.strip() or None
        try:
            rows = db.execute(
                """
                SELECT l.kratica, l.naziv, l.vrsta, l.datum,
                       snippet(laws_fts, 1, '[', ']', '...', 32) AS excerpt
                FROM laws_fts
                JOIN laws AS l ON l.id = laws_fts.rowid
                WHERE laws_fts MATCH ?
                  AND (? IS NULL OR l.vrsta = ?)
                ORDER BY rank
                LIMIT ?
                """,
                (query, vrsta_param, vrsta_param, limit)
            ).fetchall()
        except sqlite3.OperationalError as e:
            return f"FTS search error: {e}"

        if not rows:
            return f"No results for '{query}'" + (f" (vrsta={vrsta})" if vrsta else "") + "."

        lines = [f"Search results for '{query}' ({len(rows)} shown):"]
        for r in rows:
            lines.append(
                f"\n{r['kratica']} | {r['vrsta'] or '?'} | {r['datum'] or '?'}\n"
                f"  {r['naziv']}\n"
                f"  …{r['excerpt']}…"
            )
        return "\n".join(lines)

    # ── fallback: grep ────────────────────────────────────────────────────────
    try:
        out = subprocess.run(
            ["grep", "-ril", "--include=*.md", query, "si/"],
            cwd=str(REPO), capture_output=True, text=True
        ).stdout.strip()
    except Exception as e:
        return f"Search error: {e}"

    if not out:
        return f"No laws found containing '{query}'."

    files = out.splitlines()[:limit]
    results = []
    for f in files:
        path = REPO / f
        try:
            text  = path.read_text(encoding="utf-8")
            krat  = re.search(r'^kratica:\s*(.+)$', text, re.M)
            naziv = re.search(r'^naziv:\s*"(.+)"', text, re.M)
            line  = f"{krat.group(1) if krat else path.stem}: {naziv.group(1) if naziv else ''}"
        except Exception:
            line = f
        results.append(line)

    suffix = (
        f"\n(showing {len(files)} of {len(out.splitlines())} matches)"
        if len(out.splitlines()) > limit else ""
    )
    return "\n".join(results) + suffix


@mcp.tool()
def search_laws(query: str, max_results: int = 20) -> str:
    """
    Search all law texts for a term (backward-compatible alias for search()).

    query:       search string
    max_results: cap on number of matching files returned (default 20)
    """
    return search(query=query, limit=max_results)


@mcp.tool()
def list_laws(
    vrsta: str  = "",
    organ: str  = "",
    status: str = "",
    limit: int  = 100,
    offset: int = 0,
) -> str:
    """
    Browse laws with optional filters.

    vrsta:  filter by type ('zakon', 'uredba', 'pravilnik', …)
    organ:  filter by issuing body (partial match)
    status: filter by status (e.g. 'Veljaven predpis')
    limit:  max results (default 100)
    offset: pagination offset (default 0)
    """
    db = _get_db()
    if db:
        conditions = []
        params: list = []
        if vrsta.strip():
            conditions.append("vrsta = ?")
            params.append(vrsta.strip())
        if organ.strip():
            conditions.append("organ LIKE ?")
            params.append(f"%{organ.strip()}%")
        if status.strip():
            conditions.append("status LIKE ?")
            params.append(f"%{status.strip()}%")

        where = ("WHERE " + " AND ".join(conditions)) if conditions else ""
        params += [limit, offset]

        rows = db.execute(
            f"""
            SELECT kratica, naziv, vrsta, datum, organ, status
            FROM laws
            {where}
            ORDER BY datum DESC, kratica
            LIMIT ? OFFSET ?
            """,
            params
        ).fetchall()

        (total,) = db.execute(
            f"SELECT COUNT(*) FROM laws {where}",
            params[:-2]
        ).fetchone()

        if not rows:
            return "No laws found matching the given filters."

        lines = [f"Laws ({len(rows)} of {total} total, offset={offset}):"]
        for r in rows:
            lines.append(
                f"{r['kratica']} | {r['datum'] or '?'} | "
                f"{(r['naziv'] or '')[:80]}"
            )
        return "\n".join(lines)

    # ── fallback: file-based ──────────────────────────────────────────────────
    files = sorted(SI_DIR.glob("*.md"))
    results = []
    for path in files:
        try:
            text  = path.read_text(encoding="utf-8")
            krat  = re.search(r'^kratica:\s*(.+)$', text, re.M)
            naziv = re.search(r'^naziv:\s*"(.+)"', text, re.M)
            vr    = re.search(r'^vrsta:\s*"(.+)"', text, re.M)
            datum = re.search(r'^datum:\s*(.+)$', text, re.M)
            org   = re.search(r'^organ:\s*"(.+)"', text, re.M)
            stat  = re.search(r'^status:\s*"(.+)"', text, re.M)

            if vrsta and vr and vrsta.lower() not in vr.group(1).lower():
                continue
            if organ and org and organ.lower() not in org.group(1).lower():
                continue
            if status and stat and status.lower() not in stat.group(1).lower():
                continue

            line = (
                f"{krat.group(1) if krat else path.stem} | "
                f"{datum.group(1) if datum else '?'} | "
                f"{naziv.group(1)[:80] if naziv else ''}"
            )
            results.append(line)
        except Exception:
            continue
        if len(results) >= limit + offset:
            break

    paged = results[offset:offset + limit]
    if not paged:
        return f"No laws found{' of type ' + vrsta if vrsta else ''}."
    header = f"Laws ({len(paged)} shown of {len(results)} total):\n"
    return header + "\n".join(paged)


@mcp.tool()
def get_amendments(kratica: str) -> str:
    """
    Return the list of amendments for a law, sorted by date.

    kratica: base law abbreviation (e.g. 'ZKP')
    """
    db = _get_db()
    if db:
        rows = db.execute(
            """
            SELECT sprememba_kratica, sprememba_naziv, datum
            FROM amendments
            WHERE kratica = ? COLLATE NOCASE
            ORDER BY datum
            """,
            (kratica,)
        ).fetchall()

        if not rows:
            return f"No amendments found for '{kratica}' in DB."

        lines = [f"Amendments of '{kratica}' ({len(rows)} total):"]
        for r in rows:
            lines.append(
                f"  {r['datum'] or '?'}  {r['sprememba_kratica']}  —  {r['sprememba_naziv'] or ''}"
            )
        return "\n".join(lines)

    # ── fallback: parse file ──────────────────────────────────────────────────
    path = find_file(kratica)
    if path is None:
        return f"No file found for '{kratica}'."

    text = path.read_text(encoding="utf-8")
    matches = re.findall(
        r'- kratica:\s*(\S+).*?datum:\s*(\S+).*?naziv:\s*"([^"]+)"',
        text, re.S
    )
    if not matches:
        return f"No spremembe block found in {path.name}."

    lines = [f"Amendments of '{kratica}' ({len(matches)} total):"]
    for sk, sd, sn in sorted(matches, key=lambda x: x[1]):
        lines.append(f"  {sd}  {sk}  —  {sn}")
    return "\n".join(lines)


@mcp.tool()
def get_law_history(kratica: str) -> str:
    """
    Show the full amendment history of a law (all git commits touching it).

    kratica: abbreviation, e.g. 'ZKP' — also includes ZKP-A, ZKP-B, etc.
    """
    path = find_file(kratica)
    if path is None:
        return f"No file found for '{kratica}'."
    rel  = str(path.relative_to(REPO))
    stem = path.stem
    amend = f"si/{stem}-*.md"
    try:
        log = git("log", "--oneline", "--", rel, amend)
        if not log:
            return f"No git history found for {kratica}."
        count = len(log.splitlines())
        return f"History for {kratica} ({count} commits):\n{log}"
    except subprocess.CalledProcessError as e:
        return f"git error: {e.stderr}"


@mcp.tool()
def query_sql(sql: str) -> str:
    """
    Run an arbitrary read-only SQL query against trubar.db and return results.

    The query MUST start with SELECT (case-insensitive). Results are capped at
    200 rows. Useful for ad-hoc analysis: e.g. counting by vrsta, listing laws
    by organ, joining laws + amendments, etc.

    Example queries:
      SELECT vrsta, COUNT(*) FROM laws GROUP BY vrsta ORDER BY 2 DESC
      SELECT kratica, datum FROM laws WHERE organ LIKE '%Ljubljana%' LIMIT 20
      SELECT * FROM amendments WHERE sprememba_kratica = 'ZKP-N'
    """
    db = _get_db()
    if db is None:
        return "trubar.db not found — run build_db.py first."

    # Safety check: only SELECT is allowed
    if not sql.strip().upper().startswith("SELECT"):
        return "Error: only SELECT queries are allowed."

    try:
        cursor = db.execute(sql)
        rows   = cursor.fetchmany(200)
    except sqlite3.OperationalError as e:
        return f"SQL error: {e}"

    if not rows:
        return "Query returned no rows."

    cols = [d[0] for d in cursor.description]
    lines = [" | ".join(cols)]
    lines.append("-" * len(lines[0]))
    for row in rows:
        lines.append(" | ".join("" if v is None else str(v) for v in row))

    suffix = "\n(200-row cap reached)" if len(rows) == 200 else ""
    return "\n".join(lines) + suffix


# ── entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
