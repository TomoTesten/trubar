#!/usr/bin/env python3
"""
T.R.U.B.A.R. — GitHub Pages site builder
Generates docs/ from si/*.md → tomotesten.github.io/trubar

Run: python3 build_site.py
Then: npx pagefind --site docs --output-path docs/_pagefind
"""

import json, re, os, sys, html as htmllib
from pathlib import Path
import yaml
import markdown as mdlib

REPO_DIR = Path(__file__).parent
DOCS_DIR = REPO_DIR / "docs"
SI_DIR   = REPO_DIR / "si"
BASE     = "/trubar"   # GitHub Pages base (repo name)
GH_RAW   = "https://raw.githubusercontent.com/TomoTesten/trubar/master"
GH_BLOB  = "https://github.com/TomoTesten/trubar/blob/master"

# Laws that get full HTML pages (others link to GitHub raw)
FULL_PAGE_VRSTE = {"Sprejet zakon", "uredba", "pravilnik", "odredba",
                   "navodilo", "ukaz", "odlok", "drugi akt", "sklep"}

md = mdlib.Markdown(extensions=["tables", "fenced_code", "nl2br"])


# ── Parsing ────────────────────────────────────────────────────────────────────

def parse_md(path):
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return {}, ""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    try:
        front = yaml.safe_load(parts[1]) or {}
    except Exception:
        front = {}
    return front, parts[2].strip()


# ── Cross-reference engine ─────────────────────────────────────────────────────

def build_kratica_index(all_laws):
    """Returns {kratica: slug} for every known kratica."""
    idx = {}
    for slug, (front, _) in all_laws.items():
        k = front.get("kratica")
        if k:
            idx[k] = slug
    return idx


def make_crosslink_re(kratica_idx):
    """Regex that matches any known kratica as a standalone token."""
    kratice = sorted((k for k in kratica_idx if k), key=len, reverse=True)
    if not kratice:
        return None
    pat = r'(?<![A-Za-zÀ-žčšž0-9-])(' \
          + "|".join(re.escape(k) for k in kratice) \
          + r')(?![A-Za-zÀ-žčšž0-9-])'
    return re.compile(pat)


def inject_crosslinks(html_str, crosslink_re, kratica_idx, current_slug):
    """Replace kratica mentions in text nodes with <a> links."""
    if crosslink_re is None:
        return html_str

    def replace_in_text(text):
        def repl(m):
            k = m.group(1)
            slug = kratica_idx.get(k)
            if not slug or slug == current_slug:
                return k
            return f'<a href="{BASE}/si/{slug}/" class="law-ref" title="{k}">{k}</a>'
        return crosslink_re.sub(repl, text)

    # Apply only to text nodes (not inside HTML tags or attributes)
    parts = re.split(r'(<[^>]+>)', html_str)
    return "".join(replace_in_text(p) if i % 2 == 0 else p
                   for i, p in enumerate(parts))


# ── HTML helpers ───────────────────────────────────────────────────────────────

def status_badge(status):
    s = (status or "").lower()
    if "nevel" in s or "pretekl" in s:
        return '<span class="badge invalid">neveljaven</span>'
    if "vel" in s:
        return '<span class="badge valid">veljaven</span>'
    return f'<span class="badge neutral">{htmllib.escape(status or "")}</span>'


def render_law_page(slug, front, body_md, kratica_idx, crosslink_re):
    md.reset()
    body_html = md.convert(body_md)
    body_html = inject_crosslinks(body_html, crosslink_re, kratica_idx, slug)

    kratica = front.get("kratica") or slug
    naziv   = front.get("naziv") or kratica
    datum   = str(front.get("datum") or "")
    organ   = front.get("organ") or ""
    vir_url = front.get("vir") or ""
    vrsta   = front.get("vrsta") or ""
    gh_url  = f"{GH_BLOB}/si/{slug}.md"

    vir_row = f'<dt>Vir</dt><dd><a href="{htmllib.escape(vir_url)}" target="_blank">Uradni list RS</a></dd>' if vir_url else ""

    # Amendment list
    amendments = front.get("spremembe") or []
    amend_html = ""
    if amendments:
        items = []
        for a in amendments:
            ak = a.get("kratica") or ""
            an = a.get("naziv") or ak
            ad = str(a.get("datum") or "")
            target = kratica_idx.get(ak)
            link = f'<a href="{BASE}/si/{target}/">{htmllib.escape(ak)}</a>' if target else htmllib.escape(ak)
            items.append(f'<li>{link} — {htmllib.escape(an)} ({ad})</li>')
        amend_html = f'<section class="amendments"><h2>Spremembe</h2><ul>{"".join(items)}</ul></section>'

    return f"""<!DOCTYPE html>
<html lang="sl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{htmllib.escape(naziv)} — T.R.U.B.A.R.</title>
<link rel="stylesheet" href="{BASE}/style.css">
</head>
<body>
<header>
  <nav><a href="{BASE}/">← T.R.U.B.A.R.</a></nav>
  <h1 class="law-title">{htmllib.escape(naziv)}</h1>
</header>
<div class="law-container">
  <aside class="law-meta">
    <dl>
      <dt>Kratica</dt><dd><strong>{htmllib.escape(kratica)}</strong></dd>
      <dt>Vrsta</dt><dd>{htmllib.escape(vrsta)}</dd>
      <dt>Status</dt><dd>{status_badge(str(front.get("status") or ""))}</dd>
      <dt>Datum</dt><dd>{htmllib.escape(datum)}</dd>
      {"<dt>Organ</dt><dd>" + htmllib.escape(organ) + "</dd>" if organ else ""}
      {vir_row}
    </dl>
    <a href="{gh_url}" class="btn-sm" target="_blank">Prikaži na GitHub ↗</a>
  </aside>
  <article class="law-body" data-pagefind-body
           data-pagefind-meta="kratica:{htmllib.escape(kratica)},vrsta:{htmllib.escape(vrsta)}">
    {body_html}
    {amend_html}
  </article>
</div>
<footer>
  <a href="{BASE}/">Domov</a> ·
  Zakonodaja RS, javna domena (CC0) ·
  <a href="https://github.com/TomoTesten/trubar">GitHub</a>
</footer>
</body>
</html>"""


def render_list_page(title, laws_list, desc=""):
    """A simple browse/list page for a category."""
    rows = []
    for slug, front in sorted(laws_list, key=lambda x: x[1].get("naziv") or ""):
        kratica = front.get("kratica") or slug
        naziv   = front.get("naziv") or kratica
        datum   = str(front.get("datum") or "")[:10]
        st      = str(front.get("status") or "")
        badge   = status_badge(st)
        has_page = front.get("vrsta") in FULL_PAGE_VRSTE
        href    = f"{BASE}/si/{slug}/" if has_page else f"{GH_BLOB}/si/{slug}.md"
        target  = "" if has_page else ' target="_blank"'
        rows.append(
            f'<tr><td><a href="{href}"{target}>{htmllib.escape(kratica)}</a></td>'
            f'<td>{htmllib.escape(naziv)}</td>'
            f'<td>{badge}</td>'
            f'<td>{datum}</td></tr>'
        )
    return f"""<!DOCTYPE html>
<html lang="sl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{htmllib.escape(title)} — T.R.U.B.A.R.</title>
<link rel="stylesheet" href="{BASE}/style.css">
<script src="{BASE}/list-filter.js" defer></script>
</head>
<body>
<header>
  <nav><a href="{BASE}/">← T.R.U.B.A.R.</a></nav>
  <h1>{htmllib.escape(title)}</h1>
  {f'<p>{htmllib.escape(desc)}</p>' if desc else ''}
</header>
<div class="container">
  <input type="search" id="filter" placeholder="Filtriraj..." class="list-filter">
  <table class="law-table" id="law-table">
    <thead><tr><th>Kratica</th><th>Naziv</th><th>Status</th><th>Datum</th></tr></thead>
    <tbody>{"".join(rows)}</tbody>
  </table>
</div>
<footer>
  <a href="{BASE}/">Domov</a> · CC0 · <a href="https://github.com/TomoTesten/trubar">GitHub</a>
</footer>
</body>
</html>"""


def render_index(stats):
    return f"""<!DOCTYPE html>
<html lang="sl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>T.R.U.B.A.R. — Slovenski pravni red</title>
<link rel="stylesheet" href="{BASE}/style.css">
<link href="{BASE}/_pagefind/pagefind-ui.css" rel="stylesheet">
</head>
<body>
<header class="index-header">
  <h1>T.R.U.B.A.R.</h1>
  <p class="tagline">Transparentni Register Urejenih Besedil Aktov Republike</p>
  <p class="tagline-sub">Celoten slovenski pravni red — iskanje po besedilu, brskanje po zgodovini</p>
</header>

<div class="index-search">
  <div id="search"></div>
</div>

<div class="container">
  <div class="category-grid">
    <a href="{BASE}/zakoni/" class="category-card">
      <span class="cat-count">{stats['zakoni']:,}</span>
      <span class="cat-label">Zakoni</span>
    </a>
    <a href="{BASE}/uredbe/" class="category-card">
      <span class="cat-count">{stats['uredbe']:,}</span>
      <span class="cat-label">Uredbe</span>
    </a>
    <a href="{BASE}/pravilniki/" class="category-card">
      <span class="cat-count">{stats['pravilniki']:,}</span>
      <span class="cat-label">Pravilniki</span>
    </a>
    <a href="{BASE}/lokalni/" class="category-card">
      <span class="cat-count">{stats['lokalni']:,}</span>
      <span class="cat-label">Lokalni akti</span>
    </a>
    <a href="https://huggingface.co/datasets/TomoTesten/trubar-sodna-praksa"
       class="category-card hf-card" target="_blank">
      <span class="cat-count">254k</span>
      <span class="cat-label">Sodne odločbe ↗</span>
    </a>
  </div>

  <section class="about">
    <h2>O projektu</h2>
    <p>
      T.R.U.B.A.R. je arhiv celotnega slovenskega pravnega reda v strojno berljivi obliki.
      Vsak zakon je datoteka Markdown; vsaka sprememba je <em>git commit</em> — zakonodajna
      zgodovina od osamosvojitve (1991) je vidna z enim ukazom.
    </p>
    <p>
      Poimenovan po <a href="https://sl.wikipedia.org/wiki/Primo%C5%BE_Trubar">Primožu Trubarju</a>
      (1508–1586), ki je napisal prvo knjigo v slovenskem jeziku.
    </p>
    <p>
      Vir: <a href="https://pisrs.si" target="_blank">PISRS</a>,
      <a href="https://www.uradni-list.si" target="_blank">Uradni list RS</a>,
      <a href="https://fotogalerija.dz-rs.si" target="_blank">Državni zbor</a> ·
      <a href="https://github.com/TomoTesten/trubar" target="_blank">GitHub ↗</a>
    </p>
  </section>
</div>

<footer>
  CC0 javna domena · <a href="https://github.com/TomoTesten/trubar">GitHub</a> ·
  <a href="https://huggingface.co/datasets/TomoTesten/trubar-sodna-praksa">Hugging Face</a>
</footer>

<script type="module">
  import {{ PagefindUI }} from "{BASE}/_pagefind/pagefind-ui.js";
  new PagefindUI({{
    element: "#search",
    showImages: false,
    excerptLength: 25,
    translations: {{ placeholder: "Iščite zakon, člen, besedo..." }},
  }});
</script>
</body>
</html>"""


CSS = """\
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 16px; line-height: 1.6; color: #202122; background: #f8f9fa;
}

a { color: #0645ad; text-decoration: none; }
a:hover { text-decoration: underline; }

header {
  background: #fff; border-bottom: 1px solid #a7d7f9;
  padding: 12px 24px;
}
header nav a { color: #555; font-size: 14px; }

.index-header {
  background: #3366cc; color: #fff; text-align: center; padding: 48px 24px 32px;
}
.index-header h1 { font-size: 2.8rem; font-weight: 700; letter-spacing: -0.5px; }
.tagline { font-size: 1.1rem; margin-top: 8px; opacity: 0.9; }
.tagline-sub { font-size: 0.95rem; margin-top: 4px; opacity: 0.75; }

.index-search {
  background: #fff; padding: 24px; border-bottom: 1px solid #ddd;
}
.index-search > div { max-width: 720px; margin: 0 auto; }

.container { max-width: 1100px; margin: 0 auto; padding: 24px 16px; }

/* Category grid */
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  gap: 16px; margin-bottom: 32px;
}
.category-card {
  background: #fff; border: 1px solid #ddd; border-radius: 6px;
  padding: 20px 16px; text-align: center; display: flex;
  flex-direction: column; gap: 6px; transition: border-color .15s;
}
.category-card:hover { border-color: #3366cc; text-decoration: none; }
.cat-count { font-size: 1.8rem; font-weight: 700; color: #3366cc; }
.cat-label { font-size: 0.9rem; color: #555; }
.hf-card .cat-count { color: #ff9d00; }

/* About */
.about { background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 24px; }
.about h2 { margin-bottom: 12px; }
.about p { margin-bottom: 10px; color: #444; }

/* Law page layout */
.law-title { font-size: 1.4rem; margin-top: 4px; font-weight: 600; color: #202122; }

.law-container {
  max-width: 1100px; margin: 0 auto; padding: 24px 16px;
  display: grid; grid-template-columns: 240px 1fr; gap: 24px;
}
@media (max-width: 700px) {
  .law-container { grid-template-columns: 1fr; }
}

/* Sidebar */
.law-meta {
  background: #fff; border: 1px solid #ddd; border-radius: 6px;
  padding: 16px; height: fit-content;
}
.law-meta dl { display: grid; grid-template-columns: auto 1fr; gap: 4px 12px; }
.law-meta dt { font-weight: 600; color: #555; font-size: 0.85rem; white-space: nowrap; }
.law-meta dd { font-size: 0.9rem; color: #202122; }
.btn-sm {
  display: inline-block; margin-top: 16px; padding: 6px 12px;
  border: 1px solid #3366cc; border-radius: 4px; color: #3366cc;
  font-size: 0.85rem;
}
.btn-sm:hover { background: #3366cc; color: #fff; text-decoration: none; }

/* Law body */
.law-body {
  background: #fff; border: 1px solid #ddd; border-radius: 6px;
  padding: 24px 32px; min-width: 0;
}
.law-body h1, .law-body h2, .law-body h3 {
  margin: 1.2em 0 0.5em; color: #202122;
}
.law-body h1 { font-size: 1.3rem; }
.law-body h2 { font-size: 1.15rem; }
.law-body p  { margin-bottom: 0.8em; }
.law-body ul, .law-body ol { margin: 0.5em 0 0.8em 1.5em; }
.law-body table { border-collapse: collapse; width: 100%; margin: 1em 0; }
.law-body th, .law-body td { border: 1px solid #ddd; padding: 6px 10px; font-size: 0.9rem; }
.law-body th { background: #f3f4f5; }

/* Cross-reference links */
a.law-ref { color: #0645ad; border-bottom: 1px dotted #0645ad; }
a.law-ref:hover { background: #eaf3fb; }

/* Amendments */
.amendments { margin-top: 32px; padding-top: 16px; border-top: 1px solid #eee; }
.amendments h2 { font-size: 1rem; color: #555; margin-bottom: 8px; }
.amendments ul { list-style: none; }
.amendments li { padding: 4px 0; font-size: 0.9rem; border-bottom: 1px solid #f0f0f0; }

/* Badges */
.badge { padding: 2px 8px; border-radius: 3px; font-size: 0.8rem; font-weight: 600; }
.badge.valid   { background: #d4edda; color: #155724; }
.badge.invalid { background: #f8d7da; color: #721c24; }
.badge.neutral { background: #e2e3e5; color: #383d41; }

/* List pages */
.list-filter {
  width: 100%; padding: 10px 14px; border: 1px solid #ddd; border-radius: 4px;
  font-size: 1rem; margin-bottom: 16px;
}
.law-table { width: 100%; border-collapse: collapse; background: #fff; }
.law-table th { background: #f3f4f5; text-align: left; padding: 8px 12px; font-size: 0.9rem; border-bottom: 2px solid #ddd; }
.law-table td { padding: 7px 12px; border-bottom: 1px solid #f0f0f0; font-size: 0.9rem; }
.law-table tr:hover td { background: #f8f9fa; }

footer {
  text-align: center; padding: 24px; color: #555; font-size: 0.85rem;
  border-top: 1px solid #ddd; margin-top: 32px; background: #fff;
}
footer a { color: #0645ad; }
"""

LIST_FILTER_JS = """\
document.addEventListener('DOMContentLoaded', function() {
  const input = document.getElementById('filter');
  const rows  = document.querySelectorAll('#law-table tbody tr');
  if (!input) return;
  input.addEventListener('input', function() {
    const q = this.value.toLowerCase();
    rows.forEach(row => {
      row.style.display = row.textContent.toLowerCase().includes(q) ? '' : 'none';
    });
  });
});
"""


# ── Main build ─────────────────────────────────────────────────────────────────

def main():
    print("Scanning si/ (frontmatter only) ...")
    fronts = {}   # slug → front dict
    paths  = {}   # slug → Path

    for path in SI_DIR.glob("*.md"):
        front, _ = parse_md(path)   # don't keep body in memory
        slug = front.get("kratica") or path.stem
        fronts[slug] = front
        paths[slug]  = path

    print(f"  {len(fronts)} laws found")

    # Build cross-link index only from kratice that have pages (zakoni etc.)
    # — keeps the regex manageable and avoids matching obscure abbreviations
    kratica_idx = {k: k for k, f in fronts.items()
                   if f.get("kratica") and f.get("vrsta") in FULL_PAGE_VRSTE}
    crosslink_re = make_crosslink_re(kratica_idx)
    print(f"  {len(kratica_idx)} kratice for cross-linking")

    # Categorise
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
                 pravilniki=len(pravilniki), lokalni=len(lokalni))
    print(f"  zakoni={stats['zakoni']} uredbe={stats['uredbe']} "
          f"pravilniki={stats['pravilniki']} lokalni={stats['lokalni']}")

    # Create output dirs
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "si").mkdir(exist_ok=True)
    (DOCS_DIR / "zakoni").mkdir(exist_ok=True)
    (DOCS_DIR / "uredbe").mkdir(exist_ok=True)
    (DOCS_DIR / "pravilniki").mkdir(exist_ok=True)
    (DOCS_DIR / "lokalni").mkdir(exist_ok=True)

    # Write static assets
    (DOCS_DIR / "style.css").write_text(CSS)
    (DOCS_DIR / "list-filter.js").write_text(LIST_FILTER_JS)
    (DOCS_DIR / ".nojekyll").write_text("")   # disable Jekyll

    # ── Individual law pages ────────────────────────────────────────────────
    print("Generating law pages ...")
    generated = 0
    for slug, front in fronts.items():
        vrsta = front.get("vrsta") or ""
        if vrsta not in FULL_PAGE_VRSTE:
            continue
        _, body = parse_md(paths[slug])   # load body only when needed
        page_dir = DOCS_DIR / "si" / slug
        page_dir.mkdir(exist_ok=True)
        page_html = render_law_page(slug, front, body, kratica_idx, crosslink_re)
        (page_dir / "index.html").write_text(page_html, encoding="utf-8")
        generated += 1
        if generated % 500 == 0:
            print(f"  {generated} pages ...")
    print(f"  Generated {generated} law pages")

    # ── Category list pages ─────────────────────────────────────────────────
    print("Generating category pages ...")
    (DOCS_DIR / "zakoni" / "index.html").write_text(
        render_list_page("Zakoni RS", zakoni,
                         f"Vsi {len(zakoni)} veljavni in neveljavni zakoni Republike Slovenije"), "utf-8")
    (DOCS_DIR / "uredbe" / "index.html").write_text(
        render_list_page("Uredbe", uredbe), "utf-8")
    (DOCS_DIR / "pravilniki" / "index.html").write_text(
        render_list_page("Pravilniki", pravilniki), "utf-8")
    (DOCS_DIR / "lokalni" / "index.html").write_text(
        render_list_page("Lokalni akti", lokalni,
                         "Odloki, sklepi in pravilniki lokalnih skupnosti"), "utf-8")

    # ── Index ───────────────────────────────────────────────────────────────
    (DOCS_DIR / "index.html").write_text(render_index(stats), "utf-8")
    print("Generated index.html")

    print("\nDone. Now run:")
    print("  npx pagefind --site docs --output-path docs/_pagefind")
    print("Then commit and push docs/")


if __name__ == "__main__":
    main()
