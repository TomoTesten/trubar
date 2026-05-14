#!/usr/bin/env node
// Build the Pagefind static index from .pagefind-source/ (produced by
// build-search-source.mjs) and stage it at public/_pagefind so it ships with
// the Next.js app's static assets.
//
// This replaces the Phase 2 implementation that copied from docs/_pagefind.
// The new pipeline is independent of the Python build, so build_site.py can
// retire (Phase 4.6).

import { existsSync, rmSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(SCRIPT_DIR, '..');
const SOURCE = path.join(APP_ROOT, '.pagefind-source');
const TARGET = path.join(APP_ROOT, 'public', '_pagefind');

if (!existsSync(SOURCE)) {
  console.warn(
    `[pagefind] ${SOURCE} not found. Run \`node ./scripts/build-search-source.mjs\` first.`,
  );
  process.exit(0);
}

rmSync(TARGET, { recursive: true, force: true });
mkdirSync(path.dirname(TARGET), { recursive: true });

console.log('[pagefind] indexing .pagefind-source/ via npx pagefind …');
const result = spawnSync(
  'npx',
  ['--yes', 'pagefind', '--site', SOURCE, '--output-path', TARGET],
  { stdio: 'inherit' },
);
if (result.status !== 0) {
  console.error('[pagefind] failed.');
  process.exit(result.status ?? 1);
}
