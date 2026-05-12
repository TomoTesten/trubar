# T.R.U.B.A.R.

**Transparentni Register Urejenih Besedil Aktov Republike Slovenije**

Slovenian legislation as a Git repository. Every law is a Markdown file in `si/`.
Every reform is a dated git commit. spanning 1946–2026.

Named after Primož Trubar (1508–1586), who wrote the first book in the Slovenian language.

## What this repo is

- `si/*.md` — zakoni (laws), uredbe, pravilniki, odredbe, and other predpisi
- `si/npb/*.md` — Neuradna prečiščena besedila (10,042 consolidated texts from PISRS)
- Each file has YAML frontmatter: kratica, naziv, vrsta, datum, sop, organ, status, vir
- Amendment laws (e.g. `ZVO-A.md`) are separate files AND also add a reference commit to the original law's frontmatter
- Git history = legislative history: `git log si/ZKP.md` shows every time ZKP was touched

## Key files

- `fetch.py` — fetches zakoni from DZ SZ.XML → Uradni list RS → Markdown → git commit
- `fetch_podzakonski.py` — fetches uredbe/pravilniki/odredbe from PISRS Register predpisov → Uradni list RS → git commit
- `link_amendments.py` — links amendment laws to originals via frontmatter + backdated commits
- `mcp_server.py` — MCP server for querying laws by kratica, date, text search
- `build_site.py` — GitHub Pages site builder (43k+ law pages + NPB pages)
- `build_court_index.py` — builds kratica→court decisions index from HF parquet cache
- `data/SZ_fixed.XML` — source index from Državni zbor open data (3,987 laws)
- `data/court_links.json` — kratica→court decisions index (1,660 kratice, 14,576 links)

## Data sources

- Zakoni index: https://fotogalerija.dz-rs.si/datoteke/opendata/SZ.XML
- Podzakonski index: https://pisrs.si/api/filter/filter (undocumented, Register predpisov collection)
- Law texts: https://www.uradni-list.si/1/objava.jsp?sop={SOP}
- NPB texts: https://pisrs.si/pregledNpb?id={kratica}
- Court decisions: HuggingFace TomoTesten/trubar-sodna-praksa (129k+ decisions, parquet)
- Municipal ordinances: HuggingFace TomoTesten/trubar-lokalne-skupnosti (73,359 records)
- PISRS API (official consolidated texts UPB, pending access): pisrs.svz@gov.si

## Status

- [x] All 3,975 original zakoni fetched and committed
- [x] 1,207 amendment links committed
- [x] ~7,400 podzakonski akti (uredbe/pravilniki/odredbe) fetched and committed
- [x] 2023 PISRS gap fixed (522 additional items via subject-area subdivision)
- [x] Municipal ordinances uploaded to HuggingFace (73,359 records, 37 shards)
- [x] Court decision cross-links built (1,660 kratice, 14,576 links, data/court_links.json)
- [x] EU law cross-links (CELEX → EUR-Lex) injected in law pages
- [x] NPB texts (10,042) in si/npb/, exposed at /npb/ on site
- [x] AI assistant panel on every law page (Claude/ChatGPT/DeepSeek + API key mode)
- [x] GitHub Pages site live → https://tomotesten.github.io/trubar/
- [x] GitHub push → https://github.com/TomoTesten/trubar
- [x] MCP server written (mcp_server.py)
- [ ] PISRS UPB API access — email sent to pisrs.svz@gov.si, awaiting response
- [ ] Court link precision — token approach may have false positives for short kratice

## PISRS pagination note

The PISRS filter API (`/api/filter/filter`) caps cursor pagination at ~1,000 items per
query. `fetch_podzakonski.py` works around this by querying year-by-year. Years with
>900 items are further subdivided by podrocjeVsebina (subject area). All years complete.

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
