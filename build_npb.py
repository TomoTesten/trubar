#!/usr/bin/env python3
"""
T.R.U.B.A.R. — targeted NPB build
Generates docs/npb/ pages and updates docs/index.html + docs/style.css
without re-running the full 43k-page build.

Run after build_site.py has built the regular law pages.
"""
import json, sys
from pathlib import Path

# Reuse everything from build_site.py
sys.path.insert(0, str(Path(__file__).parent))
import build_site
from build_site import (
    REPO_DIR, DOCS_DIR, SI_DIR, parse_md, make_crosslink_re,
    render_law_page, render_list_page, render_index, CSS, LIST_FILTER_JS, BASE,
)


def main():
    # Load all regular-law frontmatter (for kratica_idx + crosslink_re)
    print("Scanning si/ (frontmatter only) ...")
    fronts = {}
    for path in SI_DIR.glob("*.md"):
        front, _ = parse_md(path)
        slug = front.get("kratica") or path.stem
        fronts[slug] = front
    print(f"  {len(fronts)} laws")

    kratica_idx = {k: k for k, f in fronts.items()
                   if f.get("kratica") and f.get("vrsta") in build_site.FULL_PAGE_VRSTE}
    crosslink_re = make_crosslink_re(kratica_idx)

    court_links_path = REPO_DIR / "data" / "court_links.json"
    court_links = json.loads(court_links_path.read_text()) if court_links_path.exists() else {}

    # Write per-kratica court JSON files for lazy client-side loading
    courts_dir = DOCS_DIR / "data" / "courts"
    courts_dir.mkdir(parents=True, exist_ok=True)
    for kratica_key, decisions in court_links.items():
        (courts_dir / f"{kratica_key}.json").write_text(
            json.dumps(decisions, ensure_ascii=False, separators=(",", ":")))
    print(f"  Wrote {len(court_links)} court JSON shards")

    # Scan NPB dir
    NPB_DIR = SI_DIR / "npb"
    npb_fronts = {}
    npb_paths  = {}
    for path in NPB_DIR.glob("*.md"):
        front, _ = parse_md(path)
        k = front.get("kratica") or path.stem
        if not front.get("datum") and front.get("veljaOd"):
            front["datum"] = str(front["veljaOd"])
        npb_fronts[k] = front
        npb_paths[k]  = path
    print(f"  {len(npb_fronts)} NPB texts")

    # Count stats for the index page
    by_vrsta = {}
    for slug, front in fronts.items():
        v = front.get("vrsta") or "?"
        by_vrsta.setdefault(v, []).append((slug, front))

    zakoni     = by_vrsta.get("Sprejet zakon", [])
    uredbe     = by_vrsta.get("uredba", [])
    pravilniki = by_vrsta.get("pravilnik", [])
    lokalni    = [(s, f) for v, lst in by_vrsta.items()
                  if "občinski" in v.lower() or "lokalni" in v.lower()
                  for s, f in lst]

    stats = dict(zakoni=len(zakoni), uredbe=len(uredbe),
                 pravilniki=len(pravilniki), lokalni=len(lokalni),
                 npb=len(npb_fronts))

    # Update static assets (CSS includes NPB styles)
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "style.css").write_text(CSS)
    (DOCS_DIR / "list-filter.js").write_text(LIST_FILTER_JS)
    print("Updated style.css")

    # Generate NPB pages
    (DOCS_DIR / "npb").mkdir(exist_ok=True)
    print("Generating NPB pages ...")
    npb_generated = 0
    for slug, front_npb in npb_fronts.items():
        _, body = parse_md(npb_paths[slug])
        page_dir = DOCS_DIR / "npb" / slug
        page_dir.mkdir(exist_ok=True)
        orig_slug = slug if slug in fronts else None
        page_html = render_law_page(slug, front_npb, body, kratica_idx, crosslink_re,
                                    court_links, npb=True, original_slug=orig_slug)
        (page_dir / "index.html").write_text(page_html, encoding="utf-8")
        npb_generated += 1
        if npb_generated % 1000 == 0:
            print(f"  {npb_generated} NPB pages ...")
    print(f"  Generated {npb_generated} NPB pages")

    # NPB list page
    (DOCS_DIR / "npb" / "index.html").write_text(
        render_list_page("Prečiščena besedila (NPB)",
                         list(npb_fronts.items()),
                         f"Vseh {len(npb_fronts)} neuradnih prečiščenih besedil iz PISRS",
                         page_prefix=f"{BASE}/npb"), "utf-8")
    print("Generated npb/index.html")

    # ── Export metadata for DuckDB WASM (merge regular + NPB) ───────────────
    laws_meta = []
    for slug, front in fronts.items():
        laws_meta.append({
            "kratica": front.get("kratica") or slug,
            "naziv":   (front.get("naziv") or "")[:200],
            "vrsta":   front.get("vrsta") or "",
            "datum":   str(front.get("datum") or "")[:10],
            "organ":   (front.get("organ") or "")[:100],
            "status":  str(front.get("status") or "")[:50],
            "url":     f"/trubar/si/{slug}/",
        })
    for slug, front in npb_fronts.items():
        laws_meta.append({
            "kratica": front.get("kratica") or slug,
            "naziv":   (front.get("naziv") or "")[:200],
            "vrsta":   "npb",
            "datum":   str(front.get("datum") or front.get("veljaOd") or "")[:10],
            "organ":   (front.get("organ") or "")[:100],
            "status":  str(front.get("status") or "")[:50],
            "url":     f"/trubar/npb/{slug}/",
        })
    (DOCS_DIR / "data").mkdir(exist_ok=True)
    (DOCS_DIR / "data" / "laws.json").write_text(
        json.dumps(laws_meta, ensure_ascii=False, separators=(",", ":")))
    print(f"  Wrote laws.json ({len(laws_meta)} records)")

    # Update main index.html with new stats (including npb count)
    (DOCS_DIR / "index.html").write_text(render_index(stats), "utf-8")
    print("Updated index.html")

    print(f"\nDone. NPB pages at docs/npb/ ({npb_generated} pages)")


if __name__ == "__main__":
    main()
