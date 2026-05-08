#!/usr/bin/env python3
"""
T.R.U.B.A.R. MCP server — query Slovenian legislation as a git repository.

Tools:
  get_law(kratica)               — current text of a law/act by abbreviation
  get_law_at_date(kratica, date) — text as it was on a given date (YYYY-MM-DD)
  search_laws(query)             — full-text grep across all si/*.md files
  list_laws(vrsta?)              — list all laws, optionally by type
  get_law_history(kratica)       — amendment history (git log)

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

import subprocess, re, glob, os
from pathlib import Path

from mcp.server.fastmcp import FastMCP

REPO   = Path(__file__).parent
SI_DIR = REPO / "si"

mcp = FastMCP("trubar", instructions=(
    "Query Slovenian legislation from the T.R.U.B.A.R. git repository. "
    "Laws are in si/*.md with YAML frontmatter. "
    "Git history tracks every amendment chronologically."
))


# ── helpers ────────────────────────────────────────────────────────────────────

def git(*args, check=True):
    r = subprocess.run(["git", *args], cwd=str(REPO),
                       capture_output=True, text=True, check=check)
    return r.stdout.strip()


def find_file(kratica: str) -> Path | None:
    """Find si/{kratica}.md (case-insensitive, also tries partial match)."""
    p = SI_DIR / f"{kratica}.md"
    if p.exists():
        return p
    # Try case-insensitive
    pattern = kratica.upper()
    for f in SI_DIR.glob("*.md"):
        if f.stem.upper() == pattern:
            return f
    return None


def sop_to_path(sop: str) -> Path | None:
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", sop)
    p    = SI_DIR / f"{safe}.md"
    return p if p.exists() else None


# ── tools ──────────────────────────────────────────────────────────────────────

@mcp.tool()
def get_law(kratica: str) -> str:
    """
    Return the current full text of a law or act.

    kratica: the abbreviation (e.g. 'ZKP', 'URED4488') or SOP reference.
    """
    path = find_file(kratica) or sop_to_path(kratica)
    if path is None:
        return f"No file found for '{kratica}'. Try list_laws() to browse."
    return path.read_text(encoding="utf-8")


@mcp.tool()
def get_law_at_date(kratica: str, date: str) -> str:
    """
    Return the text of a law as it was on a specific date.

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
def search_laws(query: str, max_results: int = 20) -> str:
    """
    Search all law texts for a term or phrase (case-insensitive grep).

    query:       search string
    max_results: cap on number of matching files returned (default 20)
    """
    try:
        out = subprocess.run(
            ["grep", "-ril", "--include=*.md", query, "si/"],
            cwd=str(REPO), capture_output=True, text=True
        ).stdout.strip()
    except Exception as e:
        return f"Search error: {e}"

    if not out:
        return f"No laws found containing '{query}'."

    files = out.splitlines()[:max_results]
    results = []
    for f in files:
        path = REPO / f
        # Extract frontmatter kratica + naziv
        try:
            text  = path.read_text(encoding="utf-8")
            krat  = re.search(r'^kratica:\s*(.+)$', text, re.M)
            naziv = re.search(r'^naziv:\s*"(.+)"', text, re.M)
            line  = f"{krat.group(1) if krat else path.stem}: {naziv.group(1) if naziv else ''}"
        except Exception:
            line = f
        results.append(line)

    suffix = f"\n(showing {len(files)} of {len(out.splitlines())} matches)" if len(out.splitlines()) > max_results else ""
    return "\n".join(results) + suffix


@mcp.tool()
def list_laws(vrsta: str = "", limit: int = 50) -> str:
    """
    List laws in the repository.

    vrsta:  filter by type ('zakon', 'uredba', 'pravilnik', 'odredba', etc.)
            Leave empty for all.
    limit:  max results (default 50)
    """
    files = sorted(SI_DIR.glob("*.md"))
    results = []
    for path in files:
        try:
            text  = path.read_text(encoding="utf-8")
            krat  = re.search(r'^kratica:\s*(.+)$', text, re.M)
            naziv = re.search(r'^naziv:\s*"(.+)"', text, re.M)
            vr    = re.search(r'^vrsta:\s*"(.+)"', text, re.M)
            datum = re.search(r'^datum:\s*(.+)$', text, re.M)
            if vrsta and vr and vrsta.lower() not in vr.group(1).lower():
                continue
            line = (
                f"{krat.group(1) if krat else path.stem} | "
                f"{datum.group(1) if datum else '?'} | "
                f"{naziv.group(1)[:80] if naziv else ''}"
            )
            results.append(line)
        except Exception:
            continue
        if len(results) >= limit:
            break
    if not results:
        return f"No laws found{' of type ' + vrsta if vrsta else ''}."
    total = len(files)
    header = f"{'Laws' if not vrsta else vrsta.capitalize()} ({len(results)} shown of {total} total):\n"
    return header + "\n".join(results)


@mcp.tool()
def get_law_history(kratica: str) -> str:
    """
    Show the full amendment history of a law (all git commits touching it).

    kratica: abbreviation, e.g. 'ZKP' — also includes ZKP-A, ZKP-B, etc.
    """
    path = find_file(kratica)
    if path is None:
        return f"No file found for '{kratica}'."
    rel   = str(path.relative_to(REPO))
    stem  = path.stem                          # e.g. "ZKP"
    # Include amendment files like ZKP-A.md, ZKP-B.md
    amend = f"si/{stem}-*.md"
    try:
        log = git("log", "--oneline", "--", rel, amend)
        if not log:
            return f"No git history found for {kratica}."
        count = len(log.splitlines())
        return f"History for {kratica} ({count} commits):\n{log}"
    except subprocess.CalledProcessError as e:
        return f"git error: {e.stderr}"


# ── entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")
