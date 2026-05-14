# Frozen Python build pipeline

These scripts produced the original GitHub Pages site at `docs/` and were retired in 2026 when the Next.js app at `apps/web/` took over.

Frozen as of 2026-05-14.

## Files

- `build_site.py` — main static-site generator, ~1,200 lines of f-string templating. Replaced by `apps/web/src/app/[kratica]/page.tsx`, the remark plugins in `apps/web/src/lib/`, and the RSC components in `apps/web/src/components/`.
- `build_npb.py` — fast-path for rebuilding `docs/npb/` and the home page without touching the 43k law pages. Made obsolete by ISR in the new app.
- `build-site.yml.disabled` — the GitHub Actions workflow that used to invoke these on every push. Replaced by `.github/workflows/revalidate.yml`, which only fires the Vercel revalidation API on changed paths.

## What still runs

The following scripts at the repo root are **not** legacy — they're orthogonal to the site build and continue to feed the new app:

- `fetch.py`, `fetch_dz_opendata.py`, `fetch_pisrs.py`, `fetch_podzakonski.py`, `fetch_npb.py`, `fetch_ls.py`, `fetch_court_hf.py`, `fetch_us_rs.py` — data fetchers that populate `si/*.md` and `data/`.
- `link_amendments.py` — links amendment laws to originals via frontmatter + backdated commits.
- `build_court_index.py` — produces `data/court_links.json`, which `apps/web/scripts/build-court-shards.mjs` now consumes.
- `build_db.py` — builds `trubar.db` (SQLite + FTS5) for `mcp_server.py`. Will back the paid query API in a future phase.
- `mcp_server.py` — MCP server for Claude Desktop integration.

## Rebuilding the old site (rollback)

If the new site needs to be rolled back, the old pipeline still works:

```bash
cd /path/to/trubar
python3 legacy/build_site/build_site.py
# the existing docs/ tree is overwritten in place
```

## Cleanup plan

The `docs/` tree (~1.7 GB) stays in git for 2 weeks after the new app cutover as a rollback artifact. After that, a single follow-up commit removes:

- `docs/` entirely
- `legacy/build_site/` (this directory)
