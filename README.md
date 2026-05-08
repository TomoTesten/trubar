# JOTA — Javna Odprtokodna Transparentna Arhivska zakonodaja

> Slovenian legislation as a Git repository — every law is a Markdown file, every reform is a commit.

[Jota](https://en.wikipedia.org/wiki/Jota_(stew)) is a hearty Karst stew — beans, sauerkraut, pork,
slow-cooked until everything melds together. This project does the same for Slovenian law:
takes raw legislative material, slow-cooks it into something you can actually use.

JOTA mirrors Slovenia's complete legislative corpus from independence (1991) to the present.
Each law passed by the Državni zbor (National Assembly) lives as a Markdown file.
Each amendment to that law is a dated git commit — so `git log` is Slovenia's legislative history.

## Why

- **Defence preparation**: check exactly what a law said on any date with `git show`
- **Transparency**: every legislative change is auditable — what changed, when, in what context
- **AI/LLM tooling**: plain-text corpus ready for RAG, fine-tuning, semantic search, or MCP servers
- **Academic research**: analyse amendment frequency, policy shifts, legislative velocity over time

## Structure

```
si/                    National laws (Zakoni RS)
  ZKP.md               Zakon o kazenskem postopku
  ZVO.md               Zakon o varstvu okolja
  ...
data/
  SZ.XML               Source: Državni zbor open data
fetch.py               Fetch all laws from Uradni list RS → Markdown → git commit
link_amendments.py     Link amendment laws back to their originals
```

## Usage examples

```bash
# Full text of the Criminal Procedure Act today
cat si/ZKP.md

# What did ZKP say on 1 January 2015?
git show $(git rev-list -1 --before=2015-01-01 HEAD -- si/ZKP.md):si/ZKP.md

# Full amendment history of ZKP
git log --oneline -- si/ZKP.md si/ZKP-*.md

# What exactly changed with each amendment?
git log -p -- si/ZKP.md

# All laws passed in 2022
git log --after=2022-01-01 --before=2023-01-01 --oneline

# Search all laws for a term
grep -rl "osebni podatki" si/

# Laws that were amended more than 5 times
for f in si/*.md; do
  count=$(git log --oneline -- "$f" | wc -l)
  [ "$count" -gt 5 ] && echo "$count $f"
done | sort -rn | head -20
```

## How it works

1. **Index**: [Državni zbor open data](https://fotogalerija.dz-rs.si/datoteke/opendata/SZ.XML) — 3,987 laws since 1991
2. **Text**: Fetched from [Uradni list RS](https://www.uradni-list.si) per SOP reference
3. **Format**: Markdown + YAML frontmatter (title, date, keywords, source URL, amendment list)
4. **History**: Each amendment law (`ZVO-A`, `ZKP-1B`, …) also updates the original law's
   frontmatter with an amendment entry — creating a dated commit on that file for every reform

## Reproducing from scratch

```bash
git clone <this-repo>
python3 fetch.py            # fetches all law texts, commits each backdated to publication date
python3 link_amendments.py  # links amendments to originals, commits the connections
```

## Data sources

| Source | What | Licence |
|--------|------|---------|
| [Državni zbor SZ.XML](https://fotogalerija.dz-rs.si/datoteke/opendata/SZ.XML) | Law index | CC-BY |
| [Uradni list RS](https://www.uradni-list.si) | Full law texts | Public domain |
| [PISRS](https://pisrs.si) | Consolidated texts (roadmap) | CC-BY |

## Roadmap

- [ ] Government ordinances (uredbe) and ministerial rules (pravilniki)
- [ ] PISRS consolidated texts — apply amendments automatically (seeking API key)
- [ ] Full-text search index
- [ ] MCP server — let Claude answer questions about specific articles
- [ ] English translations where available

## Contributing

Open an issue or PR. Data corrections and pipeline improvements welcome.

---

*Named after [jota](https://en.wikipedia.org/wiki/Jota_(stew)), the slow-cooked Karst stew —
because good law, like good jota, takes time, layers, and benefits from being left to develop.*
