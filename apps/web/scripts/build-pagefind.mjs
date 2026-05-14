#!/usr/bin/env node
// Build the Pagefind static index and stage it at public/_pagefind so it ships
// with the Next.js app's static assets.
//
// Source = the existing build_site.py output at ../../docs. Phase 4 (cutover)
// will switch this to index the Next.js SSG output instead, but doing it now
// avoids a chicken-and-egg with the 14k-page pre-render budget — and the
// existing 55k-page docs/ index is already what users search today.
//
// Local dev short-circuit: if docs/_pagefind already exists, just copy it,
// skipping the 3-5 minute reindex.

import { existsSync, rmSync, mkdirSync, cpSync } from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(SCRIPT_DIR, '..');
const REPO_ROOT = path.resolve(APP_ROOT, '..', '..');
const DOCS = path.join(REPO_ROOT, 'docs');
const PREBUILT = path.join(DOCS, '_pagefind');
const TARGET = path.join(APP_ROOT, 'public', '_pagefind');

if (!existsSync(DOCS)) {
  console.warn(`[pagefind] ${DOCS} not found — skipping search index.`);
  process.exit(0);
}

rmSync(TARGET, { recursive: true, force: true });
mkdirSync(path.dirname(TARGET), { recursive: true });

if (process.env.PAGEFIND_REINDEX !== '1' && existsSync(PREBUILT)) {
  console.log('[pagefind] copying existing index from docs/_pagefind …');
  cpSync(PREBUILT, TARGET, { recursive: true });
  console.log('[pagefind] done (use PAGEFIND_REINDEX=1 to force rebuild).');
  process.exit(0);
}

console.log('[pagefind] indexing docs/ via npx pagefind …');
const result = spawnSync(
  'npx',
  ['--yes', 'pagefind', '--site', DOCS, '--output-path', TARGET],
  { stdio: 'inherit' },
);
if (result.status !== 0) {
  console.error('[pagefind] failed.');
  process.exit(result.status ?? 1);
}
