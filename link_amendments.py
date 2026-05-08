#!/usr/bin/env python3
"""
JOTA - link_amendments.py

For each amendment law (e.g. ZVO-A, ZKP-1B), update the original law's
Markdown frontmatter with a 'spremembe' list and commit with the amendment's date.

This creates git history on the original law file for every amendment event,
so `git log si/ZVO.md` shows the full lifecycle of that law.

Run after fetch.py has completed.
"""

import xml.etree.ElementTree as ET
import re
import os
import subprocess
from pathlib import Path

REPO_DIR = Path(__file__).parent
SZ_XML = REPO_DIR / "data" / "SZ_fixed.XML"
LAW_DIR = REPO_DIR / "si"

# Pattern: trailing -A, -B, -AB, -1A, -1B, -2A, etc.
AMEND_SUFFIX = re.compile(r"^(.+?)[-]([A-Z]{1,2}\d?|PB)$")


def parse_all_laws():
    """Return dict kratica -> metadata, and list of amendment links."""
    tree = ET.parse(str(SZ_XML))
    root = tree.getroot()

    laws = {}
    amendments = []

    for predpis in root:
        if predpis.tag != "PREDPIS":
            continue
        card = predpis.find("KARTICA_PREDPISA")
        if card is None:
            continue

        def f(tag):
            c = card.find(tag)
            return (c.text or "").strip() if c is not None else ""

        kratica = f("KARTICA_KRATICA")
        sop = f("KARTICA_SOP")
        datum = f("KARTICA_DATUM")
        naziv = f("KARTICA_NAZIV")
        if not kratica or not datum:
            continue

        laws[kratica] = {
            "sop": sop,
            "datum": datum,
            "naziv": naziv,
        }

        m = AMEND_SUFFIX.match(kratica)
        if m:
            base = m.group(1)
            suffix = m.group(2)
            amendments.append({
                "kratica": kratica,
                "base": base,
                "suffix": suffix,
                "datum": datum,
                "sop": sop,
                "naziv": naziv,
            })

    # Sort amendments by date then suffix
    amendments.sort(key=lambda x: (x["datum"], x["suffix"]))
    return laws, amendments


def file_for(kratica):
    safe = re.sub(r"[^a-zA-Z0-9_-]", "_", kratica)
    return LAW_DIR / f"{safe}.md"


def read_frontmatter_and_body(path):
    """Parse YAML frontmatter and body from a Markdown file."""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fm_text = text[4:end]
    body = text[end + 5:]
    return fm_text, body


def update_spremembe(path, amendment):
    """Append an amendment entry to the law file's frontmatter."""
    fm_text, body = read_frontmatter_and_body(path)

    entry = f'  - kratica: {amendment["kratica"]}\n    datum: {amendment["datum"]}\n    sop: {amendment["sop"]}\n    naziv: "{amendment["naziv"]}"'

    if "spremembe:" in fm_text:
        fm_text = fm_text.rstrip() + f"\n{entry}\n"
    else:
        fm_text = fm_text.rstrip() + f"\nspremembe:\n{entry}\n"

    path.write_text(f"---\n{fm_text}---\n{body}", encoding="utf-8")


def git_commit_file(path, date_str, message):
    iso = f"{date_str}T12:00:00+01:00"
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = iso
    env["GIT_COMMITTER_DATE"] = iso
    subprocess.run(["git", "add", str(path)], cwd=str(REPO_DIR), check=True)
    result = subprocess.run(
        ["git", "commit", "-m", message],
        cwd=str(REPO_DIR), env=env, capture_output=True, text=True
    )
    return result.returncode == 0


def main():
    laws, amendments = parse_all_laws()
    print(f"Total laws: {len(laws)}, Amendments to link: {len(amendments)}")

    linked = 0
    no_base = 0
    no_file = 0

    for amend in amendments:
        kratica = amend["kratica"]
        base = amend["base"]

        if base not in laws:
            no_base += 1
            continue

        base_path = file_for(base)
        if not base_path.exists():
            no_file += 1
            continue

        amend_path = file_for(kratica)
        if not amend_path.exists():
            no_file += 1
            continue

        update_spremembe(base_path, amend)

        msg = f"[{base}] Sprememba {kratica} z dne {amend['datum']}"
        committed = git_commit_file(base_path, amend["datum"], msg)

        status = "→ linked" if committed else "→ no change"
        print(f"  {kratica} → {base} ({amend['datum']}) {status}")
        if committed:
            linked += 1

    print(f"\nDone: {linked} links committed, {no_base} missing base kratica, {no_file} missing files")


if __name__ == "__main__":
    main()
