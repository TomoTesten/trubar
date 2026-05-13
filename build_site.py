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


# Matches EU directives, regulations, decisions referenced in Slovenian law texts.
# Direktiva/Odločba/Sklep YYYY/NNN/EU|ES → EUR-Lex CELEX
# Uredba (EU|ES) YYYY/NNN → EUR-Lex CELEX
_EU_RE = re.compile(
    r'(?:'
    r'(?P<dir>Direktiva\s+(?P<dir_y>\d{4})/(?P<dir_n>\d+)/(?:ES|EU|EGS|Euratom))'
    r'|(?P<odl>Odločba\s+(?P<odl_y>\d{4})/(?P<odl_n>\d+)/(?:ES|EU|EGS))'
    r'|(?P<skl>Sklep\s+(?P<skl_y>\d{4})/(?P<skl_n>\d+)/(?:EU|ES|EGS))'
    r'|(?P<ure>Uredba\s+\((?:EU|ES|EGS|Euratom)\)\s+(?:št\.\s+)?(?P<ure_y>\d{4})/(?P<ure_n>\d+))'
    r')'
)

def inject_eu_links(html_str):
    """Replace EU law references in text nodes with EUR-Lex links."""
    def eu_repl(m):
        if m.group('dir'):
            year, num, tc = m.group('dir_y'), m.group('dir_n'), 'L'
        elif m.group('odl'):
            year, num, tc = m.group('odl_y'), m.group('odl_n'), 'D'
        elif m.group('skl'):
            year, num, tc = m.group('skl_y'), m.group('skl_n'), 'D'
        else:
            year, num, tc = m.group('ure_y'), m.group('ure_n'), 'R'
        celex = f"3{year}{tc}{int(num):04d}"
        url = f"https://eur-lex.europa.eu/legal-content/SL/TXT/?uri=CELEX:{celex}"
        return f'<a href="{url}" class="eu-ref" target="_blank" title="EUR-Lex {celex}">{m.group(0)}</a>'

    parts = re.split(r'(<[^>]+>)', html_str)
    return "".join(_EU_RE.sub(eu_repl, p) if i % 2 == 0 else p
                   for i, p in enumerate(parts))


# ── HTML helpers ───────────────────────────────────────────────────────────────

def status_badge(status):
    s = (status or "").lower()
    if "nevel" in s or "pretekl" in s:
        return '<span class="badge invalid">neveljaven</span>'
    if "vel" in s:
        return '<span class="badge valid">veljaven</span>'
    return f'<span class="badge neutral">{htmllib.escape(status or "")}</span>'


_CLEN_RE = re.compile(r'^(#{1,4})\s+(\d+)\.\s+člen\b', re.MULTILINE)

def add_article_anchors(body_md):
    """Add anchor IDs to člen headings and build TOC."""
    toc = []
    def repl(m):
        hashes, num = m.group(1), m.group(2)
        toc.append(num)
        return f'{hashes} <span id="člen-{num}">{num}. člen</span>'
    anchored = _CLEN_RE.sub(repl, body_md)
    return anchored, toc

def render_toc(toc):
    if len(toc) < 5:
        return ""
    # Group into columns of 20
    items = "".join(f'<a href="#člen-{n}">{n}</a>' for n in toc)
    return f'<nav class="toc"><strong>Členi:</strong> {items}</nav>'


def build_version_history(front, kratica_idx):
    """Return sorted list of {date, kratica, naziv, url} versions, oldest first."""
    kratica = front.get("kratica") or ""
    versions = [{
        "date":   str(front.get("datum") or "")[:10],
        "kratica": kratica,
        "naziv":  front.get("naziv") or kratica,
        "url":    f"{BASE}/si/{kratica}/",
    }]
    for a in (front.get("spremembe") or []):
        ak = a.get("kratica") or ""
        target = kratica_idx.get(ak, ak)
        versions.append({
            "date":    str(a.get("datum") or "")[:10],
            "kratica": ak,
            "naziv":   a.get("naziv") or ak,
            "url":     f"{BASE}/si/{target}/",
        })
    versions.sort(key=lambda v: v["date"])
    return versions


def render_court_decisions(decisions):
    """Render a 'Sodna praksa' section from court_links entries."""
    if not decisions:
        return ""
    items = []
    for d in decisions:
        datum  = d.get("datum") or ""
        zbirka = d.get("zbirka") or ""
        vir    = d.get("vir") or ""
        doc_id = d.get("id") or ""
        label  = f"{datum[:10]}" if datum else doc_id
        short_z = zbirka.replace("Sodna praksa ", "").replace(" sodišča", "")
        link = f'<a href="{htmllib.escape(vir)}" class="court-ref" target="_blank">{label} ({htmllib.escape(short_z)})</a>' if vir else label
        items.append(f"<li>{link}</li>")
    return (
        '<section class="court-decisions">'
        '<h2>Sodna praksa</h2>'
        f'<ul>{"".join(items)}</ul>'
        '</section>'
    )


def render_cited_by(citers, kratica_idx):
    """Render a 'Citirajo ta zakon' section."""
    if not citers:
        return ""
    items = []
    for k in sorted(citers)[:30]:  # cap at 30
        slug = kratica_idx.get(k, k)
        items.append(f'<li><a href="{BASE}/si/{slug}/" class="law-ref">{htmllib.escape(k)}</a></li>')
    more = f'<li class="more-count">… in še {len(citers)-30}</li>' if len(citers) > 30 else ""
    return (
        '<section class="cited-by">'
        '<h2>Zakoni, ki citirajo ta predpis</h2>'
        f'<ul>{"".join(items)}{more}</ul>'
        '</section>'
    )


def render_law_page(slug, front, body_md, kratica_idx, crosslink_re, court_links=None, npb=False, npb_slug=None, original_slug=None, citers=None):
    body_md, toc = add_article_anchors(body_md)
    md.reset()
    body_html = md.convert(body_md)
    body_html = inject_crosslinks(body_html, crosslink_re, kratica_idx, slug)
    body_html = inject_eu_links(body_html)
    toc_html  = render_toc(toc)

    kratica = front.get("kratica") or slug
    naziv   = front.get("naziv") or kratica
    datum   = str(front.get("datum") or front.get("veljaOd") or "")
    organ   = front.get("organ") or ""
    vir_url = front.get("vir") or ""
    vrsta   = front.get("vrsta") or ""
    npb_type = front.get("npb") or ""
    gh_path = f"si/npb/{slug}.md" if npb else f"si/{slug}.md"
    gh_url  = f"{GH_BLOB}/{gh_path}"
    gh_history_url = f"https://github.com/TomoTesten/trubar/commits/master/{gh_path}"

    vir_label = "PISRS" if npb else "Uradni list RS"
    vir_row = f'<dt>Vir</dt><dd><a href="{htmllib.escape(vir_url)}" target="_blank">{vir_label}</a></dd>' if vir_url else ""
    npb_row  = f'<dt>NPB</dt><dd>{htmllib.escape(npb_type)}</dd>' if npb_type else ""
    npb_link_row = ""
    if npb_slug:
        npb_link_row = f'<a href="{BASE}/npb/{htmllib.escape(npb_slug)}/" class="btn-action npb-link">Prečiščeno besedilo (NPB) →</a>'
    original_link_row = ""
    if original_slug:
        original_link_row = f'<a href="{BASE}/si/{htmllib.escape(original_slug)}/" class="btn-action">← Izvirno besedilo</a>'
    back_url = f"{BASE}/npb/" if npb else f"{BASE}/"

    # Version history for date picker
    versions = build_version_history(front, kratica_idx)
    versions_json = json.dumps(versions, ensure_ascii=False)

    # Amendment timeline with diff links
    amendments = front.get("spremembe") or []
    amend_html = ""
    if amendments:
        items = []
        for a in amendments:
            ak = a.get("kratica") or ""
            an = a.get("naziv") or ak
            ad = str(a.get("datum") or "")
            target = kratica_idx.get(ak, ak)
            law_link = f'<a href="{BASE}/si/{target}/" class="amend-link">{htmllib.escape(ak)}</a>'
            gh_diff  = f'<a href="https://github.com/TomoTesten/trubar/blob/master/si/{htmllib.escape(ak)}.md" class="diff-link" target="_blank" title="Besedilo spremembe na GitHubu">diff ↗</a>'
            an_short = (an[:60] + "…") if len(an) > 60 else an
            css_cls = "tl-upb" if ak.endswith("-UPB") else ("tl-other" if any(ak.endswith(s) for s in ("-ZRU", "-ZRJN", "-ZRU1")) else "")
            items.append(
                f'<li class="{css_cls}"><span class="tl-date">{ad}</span>'
                f'{law_link} <span class="tl-naziv" title="{htmllib.escape(an)}">{htmllib.escape(an_short)}</span> {gh_diff}</li>'
            )
        amend_html = (
            f'<section class="amendments">'
            f'<h2>Kronologija sprememb ({len(amendments)})'
            f' <a href="{gh_history_url}" class="history-link" target="_blank" title="Celotna git zgodovina">git ↗</a>'
            f'</h2><ul class="timeline">{"".join(items)}</ul></section>'
        )

    cited_by_html = render_cited_by(citers or [], kratica_idx)

    court_placeholder = f'<div class="court-placeholder" data-kratica="{htmllib.escape(kratica)}"></div>'

    compare_url = f"{BASE}/primerjaj/?a={htmllib.escape(kratica)}"

    naziv_json = json.dumps(naziv, ensure_ascii=False)

    ai_html = f"""<section class="ai-panel">
  <details>
    <summary class="ai-panel-title">Vprašajte umetno inteligenco o tem predpisu</summary>
    <textarea id="ai-prompt" class="ai-textarea" rows="3" spellcheck="false">Razloži mi ta predpis v preprostem jeziku. Katere so najpomembnejše določbe in kaj pomenijo v praksi?</textarea>
    <div class="ai-buttons">
      <button class="ai-btn ai-btn-claude" onclick="aiOpen('claude')">Odpri v Claudu (Anthropic)</button>
      <button class="ai-btn ai-btn-gpt" onclick="aiOpen('gpt')">Odpri v ChatGPT</button>
      <button class="ai-btn ai-btn-deepseek" onclick="aiOpen('deepseek')">Odpri v DeepSeek</button>
    </div>
    <div id="ai-copy-note" class="ai-copy-note" aria-live="polite"></div>
    <details class="ai-advanced">
      <summary>Imam lasten API ključ (napredno)</summary>
      <div class="ai-api-inner">
        <p class="ai-api-desc">
          API ključ dobite pri ponudniku (npr. <a href="https://platform.openai.com/api-keys" target="_blank">OpenAI</a>,
          <a href="https://platform.deepseek.com/" target="_blank">DeepSeek</a>).
          Ključ se hrani le v vašem brskalniku, ne zapusti vaše naprave.
          Poizvedba se izvede neposredno do ponudnika, brez posrednika.
        </p>
        <div class="ai-api-row">
          <select id="ai-provider" class="ai-select">
            <option value="openai">ChatGPT (OpenAI)</option>
            <option value="deepseek">DeepSeek</option>
            <option value="mistral">Mistral</option>
          </select>
          <input type="password" id="ai-apikey" class="ai-apikey" placeholder="API ključ (sk-...)" autocomplete="off">
          <button class="ai-send-btn" onclick="aiSendApi()">Pošlji</button>
        </div>
        <div id="ai-response" class="ai-response"></div>
      </div>
    </details>
  </details>
</section>"""

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
  <nav><a href="{back_url}">← T.R.U.B.A.R.{" / Prečiščena besedila" if npb else ""}</a></nav>
  <h1 class="law-title">{htmllib.escape(naziv)}</h1>
</header>
<div class="law-container">
  <aside class="law-meta">
    <dl>
      <dt>Kratica</dt><dd><strong>{htmllib.escape(kratica)}</strong></dd>
      <dt>Vrsta</dt><dd>{"Prečiščeno besedilo (NPB)" if npb else htmllib.escape(vrsta)}</dd>
      {"<dt>Status</dt><dd>" + status_badge(str(front.get("status") or "")) + "</dd>" if not npb else ""}
      <dt>Datum</dt><dd>{htmllib.escape(datum)}</dd>
      {"<dt>Organ</dt><dd>" + htmllib.escape(organ) + "</dd>" if organ else ""}
      {npb_row}
      {vir_row}
    </dl>

    <div class="sidebar-actions">
      {original_link_row}
      <button onclick="window.print()" class="btn-action">🖨 Natisni / PDF</button>
      <a href="{compare_url}" class="btn-action">⇄ Primerjaj</a>
      <a href="{gh_url}" class="btn-action" target="_blank">GitHub ↗</a>
      {npb_link_row}
    </div>

    <div class="date-picker-box">
      <label for="law-date"><strong>Stanje na datum:</strong></label>
      <input type="date" id="law-date" min="1991-01-01">
      <div id="date-result"></div>
    </div>
  </aside>

  <article class="law-body" data-pagefind-body
           data-pagefind-meta="kratica:{htmllib.escape(kratica)},vrsta:{htmllib.escape(vrsta)}">
    {toc_html}
    {body_html}
    {amend_html}
    {cited_by_html}
    {court_placeholder}
  </article>
</div>
<div class="ai-section-outer">
  {ai_html}
</div>
<footer>
  <a href="{BASE}/">Domov</a> ·
  Zakonodaja RS, javna domena (CC0) ·
  <a href="https://github.com/TomoTesten/trubar">GitHub</a>
</footer>
<script>
(function(){{
  var versions = {versions_json};
  var input = document.getElementById('law-date');
  var result = document.getElementById('date-result');
  function findVersion(date) {{
    var found = null;
    for (var i = 0; i < versions.length; i++) {{
      if (versions[i].date <= date) found = versions[i];
      else break;
    }}
    return found;
  }}
  function update() {{
    var d = input.value;
    if (!d) {{ result.innerHTML = ''; return; }}
    var v = findVersion(d);
    if (!v) {{
      result.innerHTML = '<p class="date-note">Zakon na ta datum še ni obstajal.</p>';
    }} else {{
      result.innerHTML = '<p class="date-note">Na dan <strong>' + d + '</strong> je veljala verzija:<br>'
        + '<a href="' + v.url + '">' + v.kratica + '</a>'
        + ' (od ' + v.date + ')</p>';
    }}
  }}
  input.addEventListener('change', update);
  // Handle ?date= query param
  var params = new URLSearchParams(window.location.search);
  if (params.get('date')) {{ input.value = params.get('date'); update(); }}
}})();

(function() {{
  var placeholder = document.querySelector('.court-placeholder[data-kratica]');
  if (!placeholder) return;
  var kratica = placeholder.getAttribute('data-kratica');
  var url = '{BASE}/data/courts/' + encodeURIComponent(kratica) + '.json';

  function renderDecisions(decisions) {{
    if (!decisions || !decisions.length) return;
    var items = decisions.map(function(d) {{
      var label = d.datum ? d.datum.slice(0,10) : d.id;
      var short_z = (d.zbirka||'').replace('Sodna praksa ','').replace(' sodišča','');
      if (d.vir) {{
        return '<li><a href="'+d.vir+'" class="court-ref" target="_blank">'+label+' ('+short_z+')</a></li>';
      }}
      return '<li>'+label+'</li>';
    }});
    var section = document.createElement('section');
    section.className = 'court-decisions';
    section.innerHTML = '<h2>Sodna praksa</h2><ul>'+items.join('')+'</ul>';
    placeholder.replaceWith(section);
  }}

  function load() {{
    fetch(url).then(function(r){{ return r.ok ? r.json() : []; }}).then(renderDecisions).catch(function(){{}});
  }}

  if ('IntersectionObserver' in window) {{
    var obs = new IntersectionObserver(function(entries) {{
      if (entries[0].isIntersecting) {{ obs.disconnect(); load(); }}
    }}, {{rootMargin: '200px'}});
    obs.observe(placeholder);
  }} else {{
    load();
  }}
}})();

(function(){{
  var lawName = {naziv_json};
  var URLS = {{
    claude:   'https://claude.ai/new',
    gpt:      'https://chatgpt.com/',
    deepseek: 'https://chat.deepseek.com/'
  }};
  var EPS = {{
    openai:   {{ url: 'https://api.openai.com/v1/chat/completions',  model: 'gpt-4o-mini' }},
    deepseek: {{ url: 'https://api.deepseek.com/chat/completions',    model: 'deepseek-chat' }},
    mistral:  {{ url: 'https://api.mistral.ai/v1/chat/completions',   model: 'mistral-small-latest' }},
  }};

  function getLawText() {{
    var el = document.querySelector('.law-body');
    return el ? el.innerText.slice(0, 5000) : '';
  }}

  window.aiOpen = function(service) {{
    var question = document.getElementById('ai-prompt').value.trim();
    var text = getLawText();
    var prompt = 'Pravni predpis: ' + lawName + '\\n\\n'
      + text.slice(0, 4000)
      + (text.length > 4000 ? '\\n[besedilo je skrajšano zaradi dolžine]\\n' : '\\n')
      + '\\nVprašanje: ' + question;
    var note = document.getElementById('ai-copy-note');
    navigator.clipboard.writeText(prompt)
      .then(function() {{
        note.textContent = 'Besedilo je bilo kopirano v odložišče. Ko se odpre pogovorno okno AI, prilepite ga (Ctrl+V oz. Cmd+V).';
        window.open(URLS[service], '_blank');
      }})
      .catch(function() {{
        window.open(URLS[service], '_blank');
      }});
  }};

  var savedKey  = localStorage.getItem('trubar_ai_key');
  var savedProv = localStorage.getItem('trubar_ai_prov');
  if (savedKey)  document.getElementById('ai-apikey').value   = savedKey;
  if (savedProv) document.getElementById('ai-provider').value = savedProv;

  window.aiSendApi = function() {{
    var provider = document.getElementById('ai-provider').value;
    var apikey   = document.getElementById('ai-apikey').value.trim();
    var question = document.getElementById('ai-prompt').value.trim();
    var respEl   = document.getElementById('ai-response');
    if (!apikey) {{ respEl.textContent = 'Prosim vnesite API ključ.'; return; }}
    localStorage.setItem('trubar_ai_key',  apikey);
    localStorage.setItem('trubar_ai_prov', provider);
    var text   = getLawText();
    var ep     = EPS[provider];
    var sysMsg = 'Si pravni asistent. Odgovarjaš vedno v slovenščini, jasno in razumljivo, brez pravnega žargona. Pomagaš pri razlagi slovenskega pravnega besedila.';
    var userMsg = 'Predpis: ' + lawName + '\\n\\n' + text.slice(0, 6000) + '\\n\\nVprašanje: ' + question;
    respEl.textContent = 'Čakam na odgovor ...';
    respEl.style.display = 'block';
    fetch(ep.url, {{
      method: 'POST',
      headers: {{ 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + apikey }},
      body: JSON.stringify({{
        model: ep.model,
        messages: [
          {{ role: 'system', content: sysMsg }},
          {{ role: 'user',   content: userMsg }}
        ],
        max_tokens: 1200,
      }})
    }}).then(function(r) {{ return r.json(); }})
      .then(function(data) {{
        var msg = (data.choices && data.choices[0] && data.choices[0].message && data.choices[0].message.content)
                  || (data.error && data.error.message)
                  || JSON.stringify(data);
        respEl.textContent = msg;
      }})
      .catch(function(e) {{ respEl.textContent = 'Napaka: ' + e.message; }});
  }};
}})();
</script>
</body>
</html>"""


def render_list_page(title, laws_list, desc="", page_prefix=None):
    """A simple browse/list page for a category."""
    if page_prefix is None:
        page_prefix = f"{BASE}/si"
    rows = []
    for slug, front in sorted(laws_list, key=lambda x: x[1].get("naziv") or ""):
        kratica = front.get("kratica") or slug
        naziv   = front.get("naziv") or kratica
        datum   = str(front.get("datum") or front.get("veljaOd") or "")[:10]
        st      = str(front.get("status") or "")
        badge   = status_badge(st)
        has_page = front.get("vrsta") in FULL_PAGE_VRSTE or front.get("npb")
        href    = f"{page_prefix}/{slug}/" if has_page else f"{GH_BLOB}/si/{slug}.md"
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
  <p class="tagline">Transparentni Register Urejenih Besedil Aktov Republike Slovenije</p>
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
    <a href="{BASE}/npb/" class="category-card">
      <span class="cat-count">{stats['npb']:,}</span>
      <span class="cat-label">Prečiščena besedila</span>
      <span class="cat-sublabel">Besedila z vgrajenimi spremembami</span>
    </a>
    <a href="https://huggingface.co/datasets/TomoTesten/trubar-sodna-praksa"
       class="category-card hf-card" target="_blank">
      <span class="cat-count">254k</span>
      <span class="cat-label">Sodne odločbe ↗</span>
      <span class="cat-sublabel">Prosto dostopna zbirka za razvoj in analizo</span>
    </a>
    <a href="{BASE}/sql/" class="category-card">
      <span class="cat-count">SQL</span>
      <span class="cat-label">Poizvedbe ↗</span>
      <span class="cat-sublabel">DuckDB v brskalniku, brez strežnika</span>
    </a>
  </div>

  <section class="recent-changes">
    <h2>Zadnje spremembe <a href="{BASE}/changelog/" class="more-link">vse →</a></h2>
    <ul id="recent-list"><li style="color:#888">Nalagam...</li></ul>
  </section>

  <section class="about">
    <h2>O projektu</h2>
    <p>
      T.R.U.B.A.R. je <strong>brezplačni, javno dostopni arhiv celotnega slovenskega pravnega reda</strong>.
      Vsebuje zakone, uredbe, pravilnike in odloke od osamosvojitve (1991) do danes.
      Besedila so brez okraskov — samo čisto besedilo, primerno za branje, iskanje in analizo.
    </p>
    <p>
      Vsak predpis ima svojo stran; v iskalno polje vpišete besedo ali frazo in takoj najdete,
      v katerem zakonu se pojavi. Vsaka sprememba zakona je zabeležena — vidite, kaj se je
      spremenilo in kdaj.
    </p>
    <p>
      <strong>Prečiščena besedila (NPB):</strong> poleg izvirnih besedil so dostopna neuradna
      prečiščena besedila, kjer so vse spremembe že vgrajene v besedilo — brez skakanja med
      osnovnim zakonom in amandmaji. Označena kot "Prečiščena besedila" v zgornjem meniju.
    </p>
    <p>
      <strong>Sodne odločbe (254.000+):</strong> zbrane odločbe Vrhovnega, Ustavnega in
      višjih sodišč so dostopne tudi kot <em>prosta zbirka za analizo in razvoj programske opreme</em>
      (gumb "Sodne odločbe ↗" zgoraj vodi na platformo HuggingFace, ki je repozitorij za
      tovrstne podatkovne zbirke — registracija ni potrebna za prenos).
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
  CC0 javna domena ·
  <a href="{BASE}/npb/">Prečiščena besedila</a> ·
  <a href="{BASE}/sql/">SQL iskanje</a> ·
  <a href="https://github.com/TomoTesten/trubar">GitHub</a> ·
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
<script>
fetch('{BASE}/data/changelog.json')
  .then(r=>r.json())
  .then(items=>{{
    document.getElementById('recent-list').innerHTML =
      items.slice(0,10).map(i=>
        `<li><span class="cl-date">${{i.date}}</span> <a href="${{i.url}}">${{i.kratica}}</a> <span class="cl-subject">${{i.subject.replace(/</g,'&lt;')}}</span></li>`
      ).join('');
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
.cat-sublabel { font-size: 0.75rem; color: #888; line-height: 1.3; }
.hf-card .cat-count { color: #ff9d00; }

/* Recent changes */
.recent-changes { background:#fff; border:1px solid #ddd; border-radius:6px; padding:20px 24px; margin-bottom:24px; }
.recent-changes h2 { font-size:1rem; margin-bottom:10px; display:flex; justify-content:space-between; align-items:center; }
.more-link { font-size:0.82rem; font-weight:400; color:#0645ad; }
.recent-changes ul { list-style:none; }
.recent-changes li { padding:5px 0; border-bottom:1px solid #f5f5f5; font-size:0.88rem; display:flex; gap:10px; align-items:baseline; }
.recent-changes li:last-child { border-bottom:none; }
.cl-date { color:#888; font-size:0.8rem; min-width:88px; flex-shrink:0; }
.cl-subject { color:#555; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }

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
  .law-body { order: -1; }
  .law-body { padding: 16px; }
  .law-body table { display: block; overflow-x: auto; -webkit-overflow-scrolling: touch; }
  .law-title { font-size: 1.1rem; }
  header { padding: 10px 16px; }
  .ai-api-row { flex-direction: column; align-items: stretch; }
  .ai-apikey, .ai-select, .ai-send-btn { width: 100%; }
  .amendments li { flex-wrap: wrap; }
  .court-decisions ul { columns: 1; }
  .ai-buttons { flex-direction: column; }
  .ai-btn { min-width: 0; }
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
a.eu-ref { color: #003399; border-bottom: 1px dotted #003399; }
a.eu-ref:hover { background: #eef2ff; }
.court-decisions { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; }
.court-decisions h2 { font-size: 1rem; color: #555; margin-bottom: 0.5rem; }
.court-decisions ul { list-style: none; padding: 0; margin: 0; columns: 2; column-gap: 1.5rem; }
.court-decisions li { font-size: 0.85rem; margin-bottom: 0.25rem; break-inside: avoid; }
a.court-ref { color: #5a2d82; }
a.court-ref:hover { text-decoration: underline; }

.cited-by { margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e0e0e0; }
.cited-by h2 { font-size: 1rem; color: #555; margin-bottom: 0.5rem; }
.cited-by ul { list-style: none; padding: 0; columns: 3; column-gap: 1rem; }
.cited-by li { font-size: 0.85rem; margin-bottom: 0.2rem; break-inside: avoid; }
.more-count { color: #888; font-style: italic; }

/* Article TOC */
.toc {
  background: #f8f9fa; border: 1px solid #ddd; border-radius: 4px;
  padding: 10px 14px; margin-bottom: 20px; font-size: 0.85rem; line-height: 1.8;
}
.toc strong { display: block; margin-bottom: 4px; color: #555; }
.toc a { color: #0645ad; margin-right: 6px; }
.toc a:hover { background: #eaf3fb; }

/* Člen anchors */
.law-body h3 span[id], .law-body h2 span[id] { scroll-margin-top: 80px; }

/* Amendments timeline */
.amendments { margin-top: 32px; padding-top: 16px; border-top: 1px solid #eee; }
.amendments h2 { font-size: 1rem; color: #555; margin-bottom: 8px; display: flex; align-items: center; gap: 8px; }
.timeline { list-style: none; padding: 0; margin: 0; position: relative; max-height: 420px; overflow-y: auto; }
.timeline::before { content: ''; position: absolute; left: 7px; top: 4px; bottom: 4px; width: 2px; background: #ddd; }
.timeline li { position: relative; padding: 4px 0 4px 26px; font-size: 0.88rem; border-bottom: none; display: block; }
.timeline li::before { content: ''; position: absolute; left: 0; top: 9px; width: 14px; height: 14px; border-radius: 50%; border: 2px solid #4a90e2; background: #fff; }
.timeline li.tl-upb::before { border-color: #8b5cf6; }
.timeline li.tl-other::before { border-color: #f59e0b; }
.timeline .tl-date { font-weight: 600; color: #333; margin-right: 6px; }
.timeline .tl-naziv { color: #666; }
.amend-link { font-weight: 600; }
.diff-link { font-size: 0.8rem; color: #999; margin-left: 4px; }
.diff-link:hover { text-decoration: underline; }
.history-link { font-size: 0.75rem; color: #888; font-weight: 400; }

/* Sidebar actions */
.sidebar-actions { display: flex; flex-direction: column; gap: 6px; margin-top: 16px; }
.btn-action {
  display: block; padding: 7px 12px; border: 1px solid #ddd; border-radius: 4px;
  background: #fff; color: #333; font-size: 0.85rem; cursor: pointer;
  text-align: center; text-decoration: none;
}
.btn-action:hover { background: #f3f4f5; border-color: #3366cc; color: #3366cc; text-decoration: none; }

/* Date picker */
.date-picker-box {
  margin-top: 16px; padding: 12px; background: #f8f9fa;
  border: 1px solid #ddd; border-radius: 4px; font-size: 0.85rem;
}
.date-picker-box label { display: block; margin-bottom: 6px; }
.date-picker-box input { width: 100%; padding: 5px 8px; border: 1px solid #ccc; border-radius: 3px; font-size: 0.85rem; }
.date-note { margin-top: 8px; font-size: 0.82rem; color: #333; line-height: 1.5; }

/* Compare page */
.compare-container { max-width: 1400px; margin: 0 auto; padding: 16px; }
.compare-controls { background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 16px; margin-bottom: 16px; display: flex; gap: 12px; align-items: flex-end; flex-wrap: wrap; }
.compare-controls label { font-size: 0.85rem; font-weight: 600; }
.compare-controls input { padding: 7px 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 0.9rem; width: 180px; }
.compare-btn { padding: 8px 20px; background: #3366cc; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 0.9rem; }
.compare-btn:hover { background: #2a55b0; }
.compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 800px) { .compare-grid { grid-template-columns: 1fr; } }
.compare-pane { background: #fff; border: 1px solid #ddd; border-radius: 6px; padding: 16px; overflow: auto; }
.compare-pane h2 { font-size: 1rem; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 1px solid #eee; }
.compare-pane .law-body-inner { font-size: 0.9rem; line-height: 1.6; }

/* AI assistant panel */
.ai-section-outer {
  max-width: 1100px; margin: 0 auto; padding: 0 16px 24px;
}
.ai-panel {
  background: #f6f8fa; border: 1px solid #d0d7de;
  border-radius: 6px; padding: 1.25rem 1.5rem;
}
.ai-panel-title { font-size: 1rem; color: #202122; list-style: none; }
.ai-panel-title::-webkit-details-marker { display: none; }
.ai-panel details > summary { cursor: pointer; }
.ai-panel details[open] > summary { margin-bottom: 0.75rem; }
.ai-textarea {
  width: 100%; border: 1px solid #ccc; border-radius: 4px;
  padding: 8px 10px; font-size: 0.9rem; resize: vertical;
  font-family: inherit; margin-bottom: 0.75rem; line-height: 1.5;
}
.ai-buttons { display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 0.6rem; }
.ai-btn {
  flex: 1 1 auto; padding: 8px 14px; border: none; border-radius: 4px;
  cursor: pointer; font-size: 0.85rem; font-weight: 600;
  transition: opacity .15s; min-width: 130px; text-align: center;
}
.ai-btn:hover { opacity: 0.82; }
.ai-btn-claude   { background: #d97706; color: #fff; }
.ai-btn-gpt      { background: #10a37f; color: #fff; }
.ai-btn-deepseek { background: #4a6cf7; color: #fff; }
.ai-copy-note {
  font-size: 0.82rem; color: #155724; min-height: 1.3em;
  padding: 4px 0; line-height: 1.4;
}
.ai-advanced { margin-top: 1rem; padding-top: 0.75rem; border-top: 1px solid #dde1e7; }
.ai-advanced summary {
  cursor: pointer; font-size: 0.85rem; color: #555; user-select: none; padding: 2px 0;
}
.ai-api-inner { margin-top: 0.75rem; }
.ai-api-desc  { font-size: 0.82rem; color: #666; margin-bottom: 0.6rem; line-height: 1.5; }
.ai-api-row   { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; margin-bottom: 0.5rem; }
.ai-select  {
  padding: 6px 8px; border: 1px solid #ccc; border-radius: 4px;
  font-size: 0.85rem; flex: 0 0 auto;
}
.ai-apikey  {
  flex: 1 1 160px; padding: 6px 8px; border: 1px solid #ccc;
  border-radius: 4px; font-size: 0.85rem; min-width: 0;
}
.ai-send-btn {
  padding: 6px 18px; background: #3366cc; color: #fff;
  border: none; border-radius: 4px; cursor: pointer; font-size: 0.85rem; white-space: nowrap;
}
.ai-send-btn:hover { background: #2a55b0; }
.ai-response {
  margin-top: 0.75rem; padding: 12px 14px; background: #fff;
  border: 1px solid #ddd; border-radius: 4px; font-size: 0.88rem;
  line-height: 1.65; white-space: pre-wrap; display: none;
}

/* Print styles */
@media print {
  header nav, .sidebar-actions, .date-picker-box, .toc, footer, .index-search,
  .ai-section-outer { display: none !important; }
  .law-container { display: block; }
  .law-meta { border: none; padding: 0; margin-bottom: 12px; }
  .law-body { border: none; padding: 0; box-shadow: none; }
  a.law-ref { color: #000; border-bottom: none; }
  a.eu-ref { color: #000; border-bottom: none; }
  .law-title { font-size: 1.2rem; }
}

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

.npb-link { background: #f0f9f0; border-color: #2e7d32; color: #2e7d32; margin-top: 4px; }
.npb-link:hover { background: #2e7d32; color: #fff; }

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

    # Build reverse citation index (which laws mention each kratica)
    print("Building reverse citation index...")
    cited_by = {}  # slug → [kratica, ...]
    for src_slug, src_front in fronts.items():
        src_vrsta = src_front.get("vrsta") or ""
        if src_vrsta not in FULL_PAGE_VRSTE:
            continue
        _, src_body = parse_md(paths[src_slug])
        if not src_body or crosslink_re is None:
            continue
        found = set(crosslink_re.findall(src_body))
        src_kratica = src_front.get("kratica") or src_slug
        for target_kratica in found:
            if target_kratica == src_kratica:
                continue
            target_slug = kratica_idx.get(target_kratica)
            if target_slug:
                cited_by.setdefault(target_slug, [])
                if src_kratica not in cited_by[target_slug]:
                    cited_by[target_slug].append(src_kratica)
    print(f"  {sum(len(v) for v in cited_by.values())} citations across {len(cited_by)} laws")

    court_links_path = REPO_DIR / "data" / "court_links.json"
    if court_links_path.exists():
        court_links = json.loads(court_links_path.read_text())
        print(f"  Loaded court links for {len(court_links)} kratice")
    else:
        court_links = {}
        print("  No court_links.json found, skipping sodna praksa links")

    # Write per-kratica court JSON files for lazy client-side loading
    courts_dir = DOCS_DIR / "data" / "courts"
    courts_dir.mkdir(parents=True, exist_ok=True)
    for kratica_key, decisions in court_links.items():
        (courts_dir / f"{kratica_key}.json").write_text(
            json.dumps(decisions, ensure_ascii=False, separators=(",", ":")))
    print(f"  Wrote {len(court_links)} court JSON shards")

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

    # ── NPB (Neuradna prečiščena besedila) ─────────────────────────────────
    NPB_DIR = SI_DIR / "npb"
    npb_fronts = {}
    npb_paths  = {}
    if NPB_DIR.exists():
        for path in NPB_DIR.glob("*.md"):
            front_npb, _ = parse_md(path)
            k = front_npb.get("kratica") or path.stem
            if not front_npb.get("datum") and front_npb.get("veljaOd"):
                front_npb["datum"] = str(front_npb["veljaOd"])
            npb_fronts[k] = front_npb
            npb_paths[k]  = path
    print(f"  {len(npb_fronts)} NPB texts found")

    # Build set of kratice that have an NPB version (for linking from regular pages)
    npb_set = set(npb_fronts.keys())

    stats = dict(zakoni=len(zakoni), uredbe=len(uredbe),
                 pravilniki=len(pravilniki), lokalni=len(lokalni),
                 npb=len(npb_fronts))
    print(f"  zakoni={stats['zakoni']} uredbe={stats['uredbe']} "
          f"pravilniki={stats['pravilniki']} lokalni={stats['lokalni']} npb={stats['npb']}")

    # Create output dirs
    DOCS_DIR.mkdir(exist_ok=True)
    (DOCS_DIR / "si").mkdir(exist_ok=True)
    (DOCS_DIR / "zakoni").mkdir(exist_ok=True)
    (DOCS_DIR / "uredbe").mkdir(exist_ok=True)
    (DOCS_DIR / "pravilniki").mkdir(exist_ok=True)
    (DOCS_DIR / "lokalni").mkdir(exist_ok=True)
    (DOCS_DIR / "npb").mkdir(exist_ok=True)

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
        _, body = parse_md(paths[slug])
        page_dir = DOCS_DIR / "si" / slug
        page_dir.mkdir(exist_ok=True)
        npb_slug = slug if slug in npb_set else None
        page_html = render_law_page(slug, front, body, kratica_idx, crosslink_re,
                                    court_links, npb_slug=npb_slug,
                                    citers=cited_by.get(slug, []))
        (page_dir / "index.html").write_text(page_html, encoding="utf-8")
        generated += 1
        if generated % 500 == 0:
            print(f"  {generated} pages ...")
    print(f"  Generated {generated} law pages")

    # ── NPB pages ───────────────────────────────────────────────────────────
    print("Generating NPB pages ...")
    npb_generated = 0
    for slug, front_npb in npb_fronts.items():
        _, body = parse_md(npb_paths[slug])
        page_dir = DOCS_DIR / "npb" / slug
        page_dir.mkdir(exist_ok=True)
        page_html = render_law_page(slug, front_npb, body, kratica_idx, crosslink_re,
                                    court_links, npb=True,
                                    original_slug=slug if slug in fronts else None)
        (page_dir / "index.html").write_text(page_html, encoding="utf-8")
        npb_generated += 1
        if npb_generated % 1000 == 0:
            print(f"  {npb_generated} NPB pages ...")
    print(f"  Generated {npb_generated} NPB pages")

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
    (DOCS_DIR / "npb" / "index.html").write_text(
        render_list_page("Prečiščena besedila (NPB)",
                         list(npb_fronts.items()),
                         f"Vseh {len(npb_fronts)} neuradnih prečiščenih besedil iz PISRS",
                         page_prefix=f"{BASE}/npb"), "utf-8")

    # ── Export metadata for DuckDB WASM ─────────────────────────────────────
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
    (DOCS_DIR / "data").mkdir(exist_ok=True)
    (DOCS_DIR / "data" / "laws.json").write_text(
        json.dumps(laws_meta, ensure_ascii=False, separators=(",", ":")))
    print(f"  Wrote laws.json ({len(laws_meta)} records)")

    # ── Index ───────────────────────────────────────────────────────────────
    (DOCS_DIR / "index.html").write_text(render_index(stats), "utf-8")
    print("Generated index.html")

    # ── Compare page ────────────────────────────────────────────────────────
    (DOCS_DIR / "primerjaj").mkdir(exist_ok=True)
    kratice_list = sorted(kratica_idx.keys())
    kratice_json = json.dumps(kratice_list, ensure_ascii=False)
    compare_page = f"""<!DOCTYPE html>
<html lang="sl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Primerjava zakonov — T.R.U.B.A.R.</title>
<link rel="stylesheet" href="{BASE}/style.css">
</head>
<body>
<header>
  <nav><a href="{BASE}/">← T.R.U.B.A.R.</a></nav>
  <h1 class="law-title">Primerjava predpisov</h1>
</header>
<div class="compare-container">
  <div class="compare-controls">
    <div>
      <label>Predpis A (kratica)</label><br>
      <input type="text" id="inp-a" placeholder="npr. ZKP" list="kratice-list">
    </div>
    <div>
      <label>Predpis B (kratica)</label><br>
      <input type="text" id="inp-b" placeholder="npr. ZUP" list="kratice-list">
    </div>
    <button class="compare-btn" onclick="compare()">Primerjaj</button>
  </div>
  <datalist id="kratice-list"></datalist>
  <div id="compare-status" style="padding:8px;color:#555;font-size:.9rem;"></div>
  <div class="compare-grid" id="compare-grid" style="display:none">
    <div class="compare-pane" id="pane-a"></div>
    <div class="compare-pane" id="pane-b"></div>
  </div>
</div>
<footer>
  <a href="{BASE}/">Domov</a> · CC0 · <a href="https://github.com/TomoTesten/trubar">GitHub</a>
</footer>
<script>
var kratice = {kratice_json};
var dl = document.getElementById('kratice-list');
kratice.forEach(function(k) {{
  var opt = document.createElement('option'); opt.value = k; dl.appendChild(opt);
}});

// Pre-fill from query params
var params = new URLSearchParams(window.location.search);
if (params.get('a')) document.getElementById('inp-a').value = params.get('a');
if (params.get('b')) document.getElementById('inp-b').value = params.get('b');
if (params.get('a') && params.get('b')) compare();

function setStatus(msg) {{ document.getElementById('compare-status').textContent = msg; }}

function fetchLawText(kratica) {{
  var url = '{BASE}/si/' + kratica + '/';
  return fetch(url)
    .then(function(r) {{
      if (!r.ok) throw new Error('Napaka pri nalaganju ' + kratica);
      return r.text();
    }})
    .then(function(html) {{
      var dp = new DOMParser();
      var doc = dp.parseFromString(html, 'text/html');
      var title = (doc.querySelector('h1.law-title') || {{}}).textContent || kratica;
      var body  = doc.querySelector('article.law-body');
      // Remove TOC and amendments for cleaner comparison
      if (body) {{
        var toc = body.querySelector('.toc');
        if (toc) toc.remove();
        var amend = body.querySelector('.amendments');
        if (amend) amend.remove();
      }}
      return {{ title: title, html: body ? body.innerHTML : '<p>Besedilo ni na voljo.</p>' }};
    }});
}}

function compare() {{
  var a = document.getElementById('inp-a').value.trim().toUpperCase();
  var b = document.getElementById('inp-b').value.trim().toUpperCase();
  if (!a || !b) {{ setStatus('Vnesite obe kratici.'); return; }}
  // Update URL
  history.replaceState(null,'','{BASE}/primerjaj/?a=' + a + '&b=' + b);
  setStatus('Nalagam ' + a + ' in ' + b + '...');
  document.getElementById('compare-grid').style.display = 'none';
  Promise.all([fetchLawText(a), fetchLawText(b)])
    .then(function(results) {{
      var pa = document.getElementById('pane-a');
      var pb = document.getElementById('pane-b');
      pa.innerHTML = '<h2>' + results[0].title + '</h2><div class="law-body-inner">' + results[0].html + '</div>';
      pb.innerHTML = '<h2>' + results[1].title + '</h2><div class="law-body-inner">' + results[1].html + '</div>';
      document.getElementById('compare-grid').style.display = 'grid';
      setStatus('');
    }})
    .catch(function(e) {{ setStatus('Napaka: ' + e.message + '. Preverite kratici.'); }});
}}
</script>
</body>
</html>"""
    (DOCS_DIR / "primerjaj" / "index.html").write_text(compare_page, "utf-8")
    print("Generated primerjaj/index.html")

    print("\nDone. Now run:")
    print("  npx pagefind --site docs --output-path docs/_pagefind")
    print("Then commit and push docs/")


if __name__ == "__main__":
    main()
