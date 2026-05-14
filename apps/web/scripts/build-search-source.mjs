#!/usr/bin/env node
// Build a minimal HTML tree at .pagefind-source/ for Pagefind to index.
// Decouples the search index from the legacy docs/ output produced by
// build_site.py — once Phase 4 cutover sticks, this is the only path that
// produces a Pagefind index.
//
// Output layout matches the new app's URL shape:
//   .pagefind-source/<kratica>/index.html      → /<kratica>
//   .pagefind-source/npb/<kratica>/index.html  → /npb/<kratica>
//
// Each file is just a body with data-pagefind-body + data-pagefind-meta. No
// site chrome, no cross-link plugins (they add link tokens that hurt retrieval
// without helping recall).

import { readdir, readFile, mkdir, writeFile, rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import matter from 'gray-matter';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(SCRIPT_DIR, '..');
const REPO_ROOT = path.resolve(APP_ROOT, '..', '..');
const SI = path.join(REPO_ROOT, 'si');
const NPB = path.join(REPO_ROOT, 'si', 'npb');
const OUT = path.join(APP_ROOT, '.pagefind-source');

const renderer = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkRehype)
  .use(rehypeStringify);

const RENDERABLE_VRSTE = new Set([
  'Sprejet zakon',
  'uredba',
  'pravilnik',
  'odredba',
  'navodilo',
  'ukaz',
  'odlok',
  'drugi akt',
  'sklep',
]);

function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"]/g, (c) =>
    c === '&' ? '&amp;' : c === '<' ? '&lt;' : c === '>' ? '&gt;' : '&quot;',
  );
}

function escapeMeta(s) {
  // data-pagefind-meta is a comma-separated k:v list; commas and colons in
  // values would break parsing. Strip them.
  return String(s ?? '').replace(/[,:]/g, ' ').slice(0, 200);
}

function year(d) {
  if (!d) return '';
  return String(d).slice(0, 4);
}

async function renderOne(srcPath, kratica, isNpb) {
  const raw = await readFile(srcPath, 'utf8');
  const parsed = matter(raw);
  const d = parsed.data ?? {};
  const naziv = String(d.naziv ?? kratica);
  const vrsta = isNpb ? 'NPB' : typeof d.vrsta === 'string' ? d.vrsta : '';

  // Only emit search docs for things we actually serve a page for. Občinski etc.
  // are linked externally — indexing them would resolve to a dead /kratica link.
  if (!isNpb && !RENDERABLE_VRSTE.has(vrsta)) return null;

  const html = String(await renderer.process(parsed.content));
  const meta = [
    `kratica:${escapeMeta(kratica)}`,
    `vrsta:${escapeMeta(vrsta)}`,
    d.organ ? `organ:${escapeMeta(d.organ)}` : null,
    d.status ? `status:${escapeMeta(d.status)}` : null,
    year(d.datum || d.veljaOd) ? `year:${year(d.datum || d.veljaOd)}` : null,
    `title:${escapeMeta(naziv)}`,
  ]
    .filter(Boolean)
    .join(',');

  const subdir = isNpb ? `npb/${kratica}` : kratica;
  const outDir = path.join(OUT, subdir);
  await mkdir(outDir, { recursive: true });
  const doc = `<!doctype html>
<html lang="sl">
<head><meta charset="utf-8"><title>${escapeHtml(naziv)}</title></head>
<body>
<article data-pagefind-body data-pagefind-meta="${meta}">
<h1>${escapeHtml(naziv)}</h1>
${html}
</article>
</body>
</html>
`;
  await writeFile(path.join(outDir, 'index.html'), doc);
  return true;
}

async function walk(dir, isNpb) {
  const files = (await readdir(dir, { withFileTypes: true }))
    .filter((d) => d.isFile() && d.name.endsWith('.md'))
    .map((d) => d.name);

  const BATCH = 100;
  let kept = 0;
  for (let i = 0; i < files.length; i += BATCH) {
    const slice = files.slice(i, i + BATCH);
    const results = await Promise.all(
      slice.map(async (name) => {
        const kratica = name.slice(0, -3);
        try {
          return await renderOne(path.join(dir, name), kratica, isNpb);
        } catch (err) {
          console.warn(`[search-source] failed ${name}:`, err.message);
          return null;
        }
      }),
    );
    kept += results.filter(Boolean).length;
    if (i % 5000 === 0 && i > 0) {
      console.log(`  …${i}/${files.length} (${kept} indexed so far)`);
    }
  }
  return kept;
}

async function main() {
  console.log('[search-source] resetting output dir …');
  await rm(OUT, { recursive: true, force: true });
  await mkdir(OUT, { recursive: true });

  console.log('[search-source] indexing si/ …');
  const lawCount = await walk(SI, false);
  console.log(`[search-source] si/ done: ${lawCount} pages.`);

  try {
    console.log('[search-source] indexing si/npb/ …');
    const npbCount = await walk(NPB, true);
    console.log(`[search-source] si/npb/ done: ${npbCount} pages.`);
  } catch {
    console.log('[search-source] no si/npb/ — skipped.');
  }
}

main().catch((err) => {
  console.error('[search-source] fatal:', err);
  process.exit(1);
});
