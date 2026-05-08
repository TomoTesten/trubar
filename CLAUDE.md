# T.R.U.B.A.R.

**Transparentni Register Urejenih Besedil Aktov Republike**

Slovenian legislation as a Git repository. Every law is a Markdown file in `si/`.
Every reform is a dated git commit. 5,195 commits spanning 1991–2026.

Named after Primož Trubar (1508–1586), who wrote the first book in the Slovenian language.

## What this repo is

- `si/*.md` — 3,973 laws passed by the Državni zbor (National Assembly) since independence
- Each file has YAML frontmatter: kratica, naziv, datum, sop, keywords, source URL
- Amendment laws (e.g. `ZVO-A.md`) are separate files AND also add a reference commit to the original law's frontmatter
- Git history = legislative history: `git log si/ZKP.md` shows every time ZKP was touched

## Key files

- `fetch.py` — fetches law texts from Uradni list RS → Markdown → git commit (run once to rebuild)
- `link_amendments.py` — links amendment laws to originals via frontmatter + backdated commits
- `data/SZ_fixed.XML` — source index from Državni zbor open data (3,987 laws)

## Data sources

- Law index: https://fotogalerija.dz-rs.si/datoteke/opendata/SZ.XML
- Law texts: https://www.uradni-list.si/1/objava.jsp?sop={SOP}
- PISRS API (consolidated texts, pending access): pisrs.svz@gov.si

## Status

- [x] All 3,975 original law texts fetched and committed
- [x] 1,207 amendment links committed
- [ ] GitHub push (repo: github.com/TomoTesten/trubar)
- [ ] PISRS API access requested — email drafted, needs sending to pisrs.svz@gov.si
- [ ] Expand to uredbe, pravilniki (government ordinances, ministerial rules)
- [ ] MCP server for querying specific articles

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

# Most amended laws
for f in si/*.md; do count=$(git log --oneline -- "$f" | wc -l); [ "$count" -gt 5 ] && echo "$count $f"; done | sort -rn | head -20
```

## Owner

Tomo Testen — tomotesten2002@gmail.com
