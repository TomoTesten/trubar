#!/usr/bin/env node
// Build per-kratica court-decision JSON shards that the CourtDecisions client
// island fetches lazily.
//
// Source: ../../data/court_links.json (1.6 MB, ~1660 kratice with 14k+ refs).
// Output: ./public/data/courts/<kratica>.json (one file per kratica).
//
// Replaces the equivalent step in build_court_index.py / build_site.py:975-980.

import { existsSync, readFileSync, rmSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(SCRIPT_DIR, '..');
const REPO_ROOT = path.resolve(APP_ROOT, '..', '..');
const SOURCE = path.join(REPO_ROOT, 'data', 'court_links.json');
const TARGET = path.join(APP_ROOT, 'public', 'data', 'courts');

if (!existsSync(SOURCE)) {
  console.warn(`[court-shards] ${SOURCE} not found — skipping.`);
  process.exit(0);
}

rmSync(TARGET, { recursive: true, force: true });
mkdirSync(TARGET, { recursive: true });

const raw = readFileSync(SOURCE, 'utf8');
const data = JSON.parse(raw);
let count = 0;
let refs = 0;
for (const [kratica, items] of Object.entries(data)) {
  if (!Array.isArray(items) || items.length === 0) continue;
  // The CourtDecisions client component expects an array of
  // { id, datum, zbirka, vir }. Pass through unchanged.
  writeFileSync(path.join(TARGET, `${kratica}.json`), JSON.stringify(items));
  count++;
  refs += items.length;
}
console.log(`[court-shards] wrote ${count.toLocaleString()} shards, ${refs.toLocaleString()} refs total.`);
