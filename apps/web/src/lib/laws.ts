import { readFile } from 'node:fs/promises';
import path from 'node:path';
import matter from 'gray-matter';
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkGfm from 'remark-gfm';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';

const REPO_ROOT = path.resolve(process.cwd(), '..', '..');

const renderer = unified()
  .use(remarkParse)
  .use(remarkGfm)
  .use(remarkRehype)
  .use(rehypeStringify);

export type LawFrontmatter = {
  kratica: string;
  naziv: string;
  vrsta?: string;
  datum?: string;
  sop?: string;
  organ?: string;
  status?: string;
  vir?: string;
  objava?: string;
  spremembe?: Array<{ kratica: string; datum: string; sop: string; naziv: string }>;
  [key: string]: unknown;
};

export async function loadLaw(kratica: string): Promise<{ frontmatter: LawFrontmatter; html: string }> {
  const file = await readFile(path.join(REPO_ROOT, 'si', `${kratica}.md`), 'utf8');
  const parsed = matter(file);
  const html = String(await renderer.process(parsed.content));
  return { frontmatter: parsed.data as LawFrontmatter, html };
}

// YAML auto-parses unquoted ISO dates into JS Date objects, so values arrive as
// either Date | string. Coerce via toJSON (works for Date, falls back to String).
export function formatLawDate(value: unknown): string | null {
  if (!value) return null;
  const s =
    typeof (value as { toJSON?: () => string }).toJSON === 'function'
      ? (value as { toJSON: () => string }).toJSON()
      : String(value);
  const match = s.match(/^\d{4}-\d{2}-\d{2}/);
  return match ? match[0] : null;
}
