# T.R.U.B.A.R.

**T**ransparentni **R**egister **U**rejenih **B**esedil **A**ktov **R**epublike

> Slovenian legislation as a Git repository — every law is a Markdown file, every amendment is a dated commit.

Named after [Primož Trubar](https://en.wikipedia.org/wiki/Primo%C5%BE_Trubar) (1508–1586), who wrote the first book in the Slovenian language. He made the written word accessible to Slovenians. This project does the same for their laws.

---

## What is this?

TRUBAR is a machine-readable, version-controlled archive of **all Slovenian legislation** — laws, regulations, ordinances, consolidated texts, parliamentary data, and court decisions — spanning from independence (1991) to the present, with selected historical documents back to 1946.

| Dataset | Records | Location |
|---|---|---|
| Zakoni RS (laws) | ~3,975 | This repo — `si/` |
| Uredbe, pravilniki, odredbe (regulations) | ~9,400 | This repo — `si/` |
| Neuradna prečiščena besedila (consolidated texts) | ~28,600 | This repo — `si/npb/` |
| Neveljavni predpisi (expired laws & regs) | ~13,900 | This repo — `si/` |
| Akti lokalnih skupnosti (municipal acts) | ~25,600 | This repo — `si/` |
| Parlamentarna vprašanja (parliamentary questions) | ~30,900 | This repo — `dz/vprasanja/` |
| Predlogi zakonov (bill proposals) | ~5,700 | This repo — `dz/predlogi_zakonov/` |
| Glasovanja (voting records) | ~29,200 | This repo — `dz/glasovanja/` |
| Seje DZ (parliamentary sessions) | ~14,300 | This repo — `dz/seje/` |
| Sodna praksa (court decisions) | ~228,000 | [HF dataset →](https://huggingface.co/datasets/TomoTesten/trubar-sodna-praksa) |
| Odločbe Ustavnega sodišča | ~25,800 | [HF dataset →](https://huggingface.co/datasets/TomoTesten/trubar-sodna-praksa) |

**Total: ~415,000 documents.**

---

## For lawyers — reading a law

Every law is a plain Markdown file readable directly on GitHub. Find the law you need:

- Browse the `si/` folder — files named by kratica (e.g. `ZKP.md` = Zakon o kazenskem postopku)
- Use GitHub's search bar at the top of this page

Each file has a YAML header with metadata, followed by the full text:

```yaml
---
kratica: ZKP
naziv: Zakon o kazenskem postopku
vrsta: zakon
datum: 1994-10-28
sop: 1994-11-0205
organ: Državni zbor RS
status: veljaven
vir: https://www.uradni-list.si/1/objava.jsp?sop=1994-11-0205
---
```

**Court decisions** are available at the [Hugging Face dataset](https://huggingface.co/datasets/TomoTesten/trubar-sodna-praksa) — browse them using the Dataset Viewer tab on that page.

---

## Web app

A read-friendly web interface lives at [trubar.vercel.app](https://trubar.vercel.app) (Next.js, Pagefind full-text search, in-page highlighter, side-by-side comparison of any two laws, per-page AI assistant). Source under [`apps/web/`](./apps/web). See [`apps/web/README.md`](./apps/web/README.md) for local dev.

The original GitHub Pages site at [tomotesten.github.io/trubar](https://tomotesten.github.io/trubar/) is preserved as a fallback; its Python build pipeline now lives at [`legacy/build_site/`](./legacy/build_site/).

---

## For developers

### Repository structure

```
si/                         All national legislation
  ZKP.md                    Zakon o kazenskem postopku
  ZKP-A.md                  Amendment A to ZKP
  npb/                      Neuradna prečiščena besedila (consolidated texts)
  MP_ODLO*.md               Municipal ordinances
dz/                         Parliamentary data (Državni zbor)
  vprasanja/                Parliamentary questions (30k+)
  predlogi_zakonov/         Bill proposals
  glasovanja/               Voting records
  seje/                     Session records
data/
  SZ_fixed.XML              Source index from Državni zbor open data
fetch.py                    Fetch zakoni → Markdown → git commit
fetch_pisrs.py              Fetch PISRS collections (regulations, NPBs, local acts)
fetch_court_hf.py           Fetch court decisions → Hugging Face dataset
fetch_dz_opendata.py        Fetch DZ parliamentary data
fetch_us_rs.py              Fetch Constitutional Court decisions
link_amendments.py          Link amendment laws to originals
mcp_server.py               MCP server for Claude Desktop integration
```

### Useful queries

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

# Most amended laws
for f in si/*.md; do
  count=$(git log --oneline -- "$f" | wc -l)
  [ "$count" -gt 5 ] && echo "$count $f"
done | sort -rn | head -20
```

### Court decisions (Hugging Face)

Court decisions are hosted as a Hugging Face dataset (too large for git at ~6 GB):

```python
from datasets import load_dataset

# Supreme, Administrative, Labour & Social Court, Higher Courts (~228k)
ds = load_dataset("TomoTesten/trubar-sodna-praksa", "sodna_praksa")

# Constitutional Court (~25.8k)
ds = load_dataset("TomoTesten/trubar-sodna-praksa", "ustavno_sodisce")
```

### MCP server (Claude Desktop)

Query laws directly from Claude:

```json
{
  "mcpServers": {
    "trubar": {
      "command": "python3",
      "args": ["/path/to/trubar/mcp_server.py"]
    }
  }
}
```

---

## Data sources

| Source | What | Licence |
|---|---|---|
| [Državni zbor SZ.XML](https://fotogalerija.dz-rs.si/datoteke/opendata/SZ.XML) | Law index | CC-BY |
| [Uradni list RS](https://www.uradni-list.si) | Full law texts | Public domain |
| [PISRS Register predpisov](https://pisrs.si) | Regulations, consolidated texts, local acts | CC-BY |
| [sodnapraksa.si](https://sodnapraksa.si) | Court decisions | Public domain |
| [us-rs.si](https://www.us-rs.si) | Constitutional Court decisions | Public domain |
| [DZ open data](https://fotogalerija.dz-rs.si/datoteke/opendata/) | Parliamentary data | CC-BY |

All source texts are official public records of the Republic of Slovenia.

---

## Licence

**CC0 1.0 — public domain.** The law belongs to everyone.

---

## Roadmap

- [x] Full-text search web interface (Next.js + Pagefind at apps/web/)
- [x] EU law cross-references (EUR-Lex CELEX IDs)
- [ ] Automatic weekly sync via GitHub Actions
- [ ] Auth + paid tier (Better Auth + Polar.sh) for API access, alerts, saved searches
- [ ] Surface dz/ corpus (votes / parliamentary questions / bill proposals) on law pages
- [ ] ECHR Slovenia cases
- [ ] English translations where available

---

## Contributing

Open an issue or PR. Data corrections and pipeline improvements welcome.

**Maintainer:** Tomo Testen — tomotesten2002@gmail.com

---

*"Ta naš jezik je ta stari slovenski jezik." — Primož Trubar*
*("This our language is the old Slovenian language.")*
