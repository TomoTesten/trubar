import { readFile, readdir } from 'node:fs/promises';
import path from 'node:path';
import matter from 'gray-matter';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';
import { z } from 'zod';
import { remarkKraticaLinks } from './remark-kratica-links';
import { remarkEuLinks } from './remark-eu-links';

const REPO_ROOT = path.resolve(process.cwd(), '..', '..');

function buildRenderer(kraticaIndex: Map<string, string>, current: string) {
  return unified()
    .use(remarkParse)
    .use(remarkGfm)
    .use(remarkKraticaLinks, { index: kraticaIndex, current })
    .use(remarkEuLinks)
    .use(remarkRehype)
    .use(rehypeStringify);
}

// YAML auto-parses unquoted ISO dates into JS Date objects. Coerce everything to
// YYYY-MM-DD strings at the schema boundary so the rest of the app sees one type.
const dateString = z.preprocess(
  (v) => {
    if (v == null) return undefined;
    const s =
      typeof (v as { toJSON?: () => string }).toJSON === 'function'
        ? (v as { toJSON: () => string }).toJSON()
        : String(v);
    const m = s.match(/^\d{4}-\d{2}-\d{2}/);
    return m ? m[0] : undefined;
  },
  z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
);

const amendmentSchema = z.object({
  kratica: z.string(),
  datum: dateString,
  sop: z.string().optional(),
  naziv: z.string().optional(),
});

export const lawFrontmatterSchema = z.object({
  kratica: z.string(),
  naziv: z.string(),
  vrsta: z.string().optional(),
  datum: dateString,
  sop: z.string().optional(),
  organ: z.string().optional(),
  status: z.string().optional(),
  vir: z.string().url().optional(),
  objava: z.string().optional(),
  zbirka: z.string().optional(),
  kljucne_besede: z.array(z.string()).optional(),
  npb: z.string().optional(),
  veljaOd: dateString,
  spremembe: z.array(amendmentSchema).optional(),
});

export type LawFrontmatter = z.infer<typeof lawFrontmatterSchema>;

// The URL slug (filename minus .md) is the source of truth for kratica. The YAML
// `kratica:` field can be blank (e.g. older 1991_01_NNNN-style files) — fall back
// to the filename in that case.
export async function loadLaw(
  kratica: string,
): Promise<{ frontmatter: LawFrontmatter; html: string }> {
  return loadFromPath(path.join(REPO_ROOT, 'si', `${kratica}.md`), kratica);
}

export async function loadNpb(
  kratica: string,
): Promise<{ frontmatter: LawFrontmatter; html: string }> {
  return loadFromPath(path.join(REPO_ROOT, 'si', 'npb', `${kratica}.md`), kratica);
}

async function loadFromPath(filePath: string, kratica: string) {
  const file = await readFile(filePath, 'utf8');
  const parsed = matter(file);
  const frontmatter = lawFrontmatterSchema.parse({ ...parsed.data, kratica });
  const index = await getKraticaIndex();
  const renderer = buildRenderer(index, kratica);
  const html = String(await renderer.process(parsed.content));
  return { frontmatter, html };
}

let _kraticaIndexPromise: Promise<Map<string, string>> | null = null;

// Cross-link target index: kratica → URL slug. Only includes entries whose
// frontmatter advertises a real kratica field, matching build_site.py:50-57.
export function getKraticaIndex(): Promise<Map<string, string>> {
  if (!_kraticaIndexPromise) {
    _kraticaIndexPromise = (async () => {
      const manifest = await getLawManifest();
      const idx = new Map<string, string>();
      for (const entry of manifest) {
        // The manifest's kratica field is filename-derived; we want the YAML one
        // so cross-links match references in body text (e.g. "ZKP" not "1991_01...").
        const k = entry.kratica;
        // Heuristic guard against using filename-style kratice as link targets.
        // Real kratice are typically ALL-CAPS abbreviations under ~15 chars.
        if (k && /^[A-ZČŠŽ][A-ZČŠŽa-z0-9-]{0,14}$/.test(k)) {
          idx.set(k, k);
        }
      }
      return idx;
    })();
  }
  return _kraticaIndexPromise;
}

// Per build_site.py:23 — vrsta values that warrant a full page rather than just a
// listing entry. Used to scope SSG and ISR generation.
export const RENDERABLE_VRSTE = new Set([
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

export type ManifestEntry = {
  kratica: string;
  vrsta?: string;
  naziv: string;
  datum?: string;
  status?: string;
};

let _manifestPromise: Promise<ManifestEntry[]> | null = null;

export function getLawManifest(): Promise<ManifestEntry[]> {
  if (!_manifestPromise) _manifestPromise = scanLaws();
  return _manifestPromise;
}

async function scanLaws(): Promise<ManifestEntry[]> {
  const dir = path.join(REPO_ROOT, 'si');
  const files = (await readdir(dir, { withFileTypes: true }))
    .filter((d) => d.isFile() && d.name.endsWith('.md'))
    .map((d) => d.name);

  // Read in batches to avoid file-descriptor exhaustion on the 108k-file corpus.
  const BATCH = 200;
  const out: ManifestEntry[] = [];
  for (let i = 0; i < files.length; i += BATCH) {
    const slice = files.slice(i, i + BATCH);
    const batch = await Promise.all(
      slice.map(async (name) => {
        const kratica = name.slice(0, -3);
        try {
          // Only read enough to capture frontmatter (typically <1 KB).
          const raw = await readFile(path.join(dir, name), 'utf8');
          const parsed = matter(raw);
          const d = parsed.data as Record<string, unknown>;
          if (!d.naziv) return null;
          return {
            kratica,
            vrsta: typeof d.vrsta === 'string' ? d.vrsta : undefined,
            naziv: String(d.naziv),
            datum:
              typeof d.datum === 'string'
                ? d.datum.slice(0, 10)
                : d.datum instanceof Date
                  ? d.datum.toISOString().slice(0, 10)
                  : undefined,
            status: typeof d.status === 'string' ? d.status : undefined,
          } satisfies ManifestEntry;
        } catch {
          return null;
        }
      }),
    );
    for (const entry of batch) if (entry) out.push(entry);
  }
  return out;
}
