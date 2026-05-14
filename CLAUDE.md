# T.R.U.B.A.R.

**Transparentni Register Urejenih Besedil Aktov Republike Slovenije**

Slovenian legislation as a Git repository. Every law is a Markdown file in `si/`.
Every reform is a dated git commit. Spanning 1946–2026.

Named after Primož Trubar (1508–1586), who wrote the first book in the Slovenian language.

## What this repo is

- `si/*.md` — zakoni (laws), uredbe, pravilniki, odredbe, and other predpisi
- `si/npb/*.md` — Neuradna prečiščena besedila (10,042 consolidated texts from PISRS)
- Each file has YAML frontmatter: kratica, naziv, vrsta, datum, sop, organ, status, vir
- Amendment laws (e.g. `ZVO-A.md`) are separate files AND also add a reference commit to the original law's frontmatter
- Git history = legislative history: `git log si/ZKP.md` shows every time ZKP was touched

## Architecture (as of 2026)

The site is a **Next.js 16 App Router** app under `apps/web/`, deployed to Vercel.
Hybrid rendering: ~14k pages pre-rendered at build (3,975 Sprejet zakon + 10,042 NPB
when `SSG_FULL=1`), the long tail (~40k občinski / akt / sklep) served via ISR.

The previous Python static-site pipeline (`build_site.py`, `build_npb.py`) is frozen
at `legacy/build_site/` — see its README for rollback instructions.

### Key app files

- `apps/web/src/app/[kratica]/page.tsx` — main law detail route (SSG + ISR)
- `apps/web/src/app/npb/[kratica]/page.tsx` — NPB detail
- `apps/web/src/app/{zakoni,uredbe,pravilniki,npb,lokalni}/page.tsx` — listings
- `apps/web/src/app/primerjaj/page.tsx` — compare two laws
- `apps/web/src/lib/laws.ts` — frontmatter Zod schema, manifest scan, remark pipeline
- `apps/web/src/lib/remark-kratica-links.ts` — kratica cross-links (port of build_site.py:60-105)
- `apps/web/src/lib/remark-eu-links.ts` — EU CELEX cross-links
- `apps/web/src/components/SearchCommand.tsx` — global ⌘K palette over Pagefind
- `apps/web/src/components/AiPanel.tsx` — per-law AI assistant
- `apps/web/scripts/build-search-source.mjs` — renders `si/*.md` into `.pagefind-source/`
- `apps/web/scripts/build-pagefind.mjs` — runs `pagefind` over that source
- `apps/web/scripts/build-court-shards.mjs` — splits `data/court_links.json` into per-kratica JSON

### Build + deploy

```bash
cd apps/web
bun install
bun run dev     # http://localhost:3000, dev with SSG capped at 25 pages

# Full prod-shape build (~5 min postbuild for Pagefind):
SSG_FULL=1 bun run build
bun run start
```

Vercel env vars (Production):
- `SSG_FULL=1` — pre-render all 14k hot pages
- `NEXT_PUBLIC_SITE_URL` — absolute base URL used by sitemap/robots
- `REVALIDATE_TOKEN` — shared secret for the ISR webhook (matches GitHub secret)

GitHub Actions secrets:
- `SITE_URL` — base URL of the deployed app (e.g. https://trubar.vercel.app)
- `REVALIDATE_TOKEN` — same secret as above; `.github/workflows/revalidate.yml`
  POSTs changed paths to `/api/revalidate` on every push to master.

## Non-site scripts (still active)

- `fetch.py` — fetches zakoni from DZ SZ.XML → Uradni list RS → Markdown → git commit
- `fetch_podzakonski.py` — fetches uredbe/pravilniki/odredbe from PISRS Register predpisov
- `fetch_npb.py`, `fetch_ls.py`, `fetch_pisrs.py`, `fetch_dz_opendata.py`, `fetch_court_hf.py`, `fetch_us_rs.py` — other data fetchers
- `link_amendments.py` — links amendment laws to originals via frontmatter + backdated commits
- `build_court_index.py` — produces `data/court_links.json` (consumed by `build-court-shards.mjs`)
- `build_db.py` — builds `trubar.db` (SQLite + FTS5) for the MCP server
- `mcp_server.py` — MCP server for Claude Desktop integration

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
- [x] 10,042 NPB texts committed
- [x] Next.js 16 app at apps/web/ (Phase 0-4 of the modernization)
- [x] Pagefind index built from si/*.md directly (no longer depends on docs/)
- [x] Court decision cross-links per-kratica JSON shards
- [x] Compare tool (/primerjaj) using react-diff-viewer-continued
- [x] Global ⌘K command palette
- [x] In-page search highlighter
- [x] Branded 404, sitemap.xml, robots.txt, OG image
- [ ] Legacy `build_site.py` pipeline retired at `legacy/build_site/` (keep for 2 weeks as rollback)
- [ ] PISRS UPB API access — email sent to pisrs.svz@gov.si, awaiting response
- [ ] Court link precision — token approach may have false positives for short kratice
- [ ] Auth + paid tier (planned follow-up phase: Better Auth + Polar.sh)

## PISRS pagination note

The PISRS filter API (`/api/filter/filter`) caps cursor pagination at ~1,000 items per
query. `fetch_podzakonski.py` works around this by querying year-by-year. Years with
>900 items are further subdivided by podrocjeVsebina (subject area).

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

# Most amended laws
for f in si/*.md; do count=$(git log --oneline -- "$f" | wc -l); [ "$count" -gt 5 ] && echo "$count $f"; done | sort -rn | head -20

# Force-rebuild the Pagefind source (skips the dev short-circuit)
cd apps/web && PAGEFIND_REINDEX=1 bun run build

# Rebuild the old Python site (rollback path)
python3 legacy/build_site/build_site.py
```

## Owner

Tomo Testen — tomotesten2002@gmail.com
