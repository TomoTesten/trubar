# T.R.U.B.A.R.

**Transparentni Register Urejenih Besedil Aktov Republike**

Slovenian legislation as a Git repository. Every law is a Markdown file in `si/`.
Every reform is a dated git commit. 5,196+ commits spanning 1946–2026.

Named after Primož Trubar (1508–1586), who wrote the first book in the Slovenian language.

## What this repo is

- `si/*.md` — zakoni (laws), uredbe, pravilniki, odredbe, and other predpisi
- Each file has YAML frontmatter: kratica, naziv, vrsta, datum, sop, organ, status, vir
- Amendment laws (e.g. `ZVO-A.md`) are separate files AND also add a reference commit to the original law's frontmatter
- Git history = legislative history: `git log si/ZKP.md` shows every time ZKP was touched

## Key files

- `fetch.py` — fetches zakoni from DZ SZ.XML → Uradni list RS → Markdown → git commit
- `fetch_podzakonski.py` — fetches uredbe/pravilniki/odredbe from PISRS Register predpisov → Uradni list RS → git commit
- `link_amendments.py` — links amendment laws to originals via frontmatter + backdated commits
- `mcp_server.py` — MCP server for querying laws by kratica, date, text search
- `data/SZ_fixed.XML` — source index from Državni zbor open data (3,987 laws)

## Data sources

- Zakoni index: https://fotogalerija.dz-rs.si/datoteke/opendata/SZ.XML
- Podzakonski index: https://pisrs.si/api/filter/filter (undocumented, Register predpisov collection)
- Law texts: https://www.uradni-list.si/1/objava.jsp?sop={SOP}
- PISRS API (consolidated texts, pending access): pisrs.svz@gov.si

## Status

- [x] All 3,975 original law texts fetched and committed
- [x] 1,207 amendment links committed
- [x] GitHub push → https://github.com/TomoTesten/trubar
- [x] MCP server written (mcp_server.py)
- [ ] fetch_podzakonski.py running — ~7,400 uredbe/pravilniki/odredbe being fetched overnight
- [ ] Push uredbe/pravilniki commits to GitHub after fetch completes
- [ ] PISRS API access requested — email needs sending to pisrs.svz@gov.si
- [ ] Expand to predpisi lokalnih skupnosti (municipal ordinances)

## PISRS pagination note

The PISRS filter API (`/api/filter/filter`) caps cursor pagination at ~1,000 items per
query. `fetch_podzakonski.py` works around this by querying year-by-year. The only year
affected is 2023 (1,279 items; we get ~1,000). All other years are complete.

## MCP server setup (Claude Desktop)

Add to `~/.claude.json` or Claude Desktop settings:
```json
{
  "mcpServers": {
    "trubar": {
      "command": "python3",
      "args": ["/data/T.R.U.B.A.R./mcp_server.py"]
    }
  }
}
```

## Useful commands

```bash
# What did ZKP say on 1 Jan 2015?
git show $(git rev-list -1 --before=2015-01-01 HEAD -- si/ZKP.md):si/ZKP.md

# Full amendment history of a law
git log --oneline -- si/ZKP.md si/ZKP-*.md

# What changed with each amendment?
git log -p -- si/ZKP.md

# Search all laws for a term
grep -rl "osebni podatki" si/

# List all uredbe
grep -rl '^vrsta: "uredba"' si/ | wc -l

# Most amended laws
for f in si/*.md; do count=$(git log --oneline -- "$f" | wc -l); [ "$count" -gt 5 ] && echo "$count $f"; done | sort -rn | head -20

# Re-run podzakonski fetch (resumes from progress file)
python3 fetch_podzakonski.py

# Push to GitHub (requires setting token in remote URL first)
# git remote set-url origin https://TOKEN@github.com/TomoTesten/trubar.git
# git push origin master
```

## Owner

Tomo Testen — tomotesten2002@gmail.com
