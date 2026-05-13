#!/usr/bin/env python3
"""Generate docs/data/changelog.json from git log of si/ commits."""
import json, subprocess, re
from pathlib import Path

REPO_DIR = Path(__file__).parent
OUT = REPO_DIR / "docs" / "data" / "changelog.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

def main():
    # Get last 500 commits touching si/ with date, subject, files
    result = subprocess.run(
        ["git", "log", "--format=%H|%aI|%s", "--name-only",
         "--diff-filter=AM", "-500", "--", "si/*.md", "si/npb/*.md"],
        cwd=str(REPO_DIR), capture_output=True, text=True
    )
    entries = []
    current = None
    for line in result.stdout.splitlines():
        if "|" in line and len(line.split("|")) >= 3:
            if current and current.get("files"):
                entries.append(current)
            parts = line.split("|", 2)
            current = {"hash": parts[0][:8], "date": parts[1][:10], "subject": parts[2], "files": []}
        elif line.strip().endswith(".md") and current:
            current["files"].append(line.strip())
    if current and current.get("files"):
        entries.append(current)

    # Flatten to per-file entries, cap at 200
    flat = []
    seen = set()
    for e in entries:
        for f in e["files"]:
            kratica = Path(f).stem
            if kratica in seen:
                continue
            seen.add(kratica)
            is_npb = "npb/" in f
            flat.append({
                "kratica": kratica,
                "date": e["date"],
                "subject": e["subject"],
                "url": f"/trubar/npb/{kratica}/" if is_npb else f"/trubar/si/{kratica}/",
                "hash": e["hash"],
            })
            if len(flat) >= 200:
                break
        if len(flat) >= 200:
            break

    OUT.write_text(json.dumps(flat, ensure_ascii=False, separators=(",", ":")))
    print(f"Written {len(flat)} entries → {OUT}")

if __name__ == "__main__":
    main()
