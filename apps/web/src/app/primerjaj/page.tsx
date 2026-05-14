import type { Metadata } from 'next';
import { readFile } from 'node:fs/promises';
import path from 'node:path';
import matter from 'gray-matter';
import { getLawManifest, RENDERABLE_VRSTE } from '@/lib/laws';
import { DiffViewer } from '@/components/DiffViewer';

export const metadata: Metadata = { title: 'Primerjaj predpisa' };
export const revalidate = 3600;

const REPO_ROOT = path.resolve(process.cwd(), '..', '..');

async function loadBody(kratica: string): Promise<string | null> {
  // Try plain law first, fall back to NPB.
  for (const subdir of ['si', 'si/npb']) {
    try {
      const raw = await readFile(path.join(REPO_ROOT, subdir, `${kratica}.md`), 'utf8');
      return matter(raw).content;
    } catch {
      // try next
    }
  }
  return null;
}

export default async function Page(props: PageProps<'/primerjaj'>) {
  const params = await props.searchParams;
  const a = typeof params.a === 'string' ? params.a : '';
  const b = typeof params.b === 'string' ? params.b : '';

  const manifest = await getLawManifest();
  const candidates = manifest
    .filter((e) => e.vrsta && RENDERABLE_VRSTE.has(e.vrsta))
    .sort((x, y) => x.kratica.localeCompare(y.kratica, 'sl'));

  const [bodyA, bodyB] = await Promise.all([
    a ? loadBody(a) : Promise.resolve(null),
    b ? loadBody(b) : Promise.resolve(null),
  ]);

  return (
    <main className="mx-auto max-w-7xl px-4 py-6">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">Primerjaj predpisa</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Vnesite dve kratici (npr. ZKP in ZKP-A) za prikaz razlik med besediloma.
        </p>
      </header>

      <form className="mb-6 flex flex-wrap items-end gap-3" method="get">
        <label className="flex flex-col gap-1 text-xs">
          <span className="text-muted-foreground">Levo</span>
          <input
            name="a"
            list="kratice"
            defaultValue={a}
            placeholder="ZKP"
            className="min-w-[200px] rounded-md border border-border bg-background px-3 py-1.5 text-sm font-mono"
          />
        </label>
        <label className="flex flex-col gap-1 text-xs">
          <span className="text-muted-foreground">Desno</span>
          <input
            name="b"
            list="kratice"
            defaultValue={b}
            placeholder="ZKP-A"
            className="min-w-[200px] rounded-md border border-border bg-background px-3 py-1.5 text-sm font-mono"
          />
        </label>
        <button
          type="submit"
          className="rounded-md border border-border bg-card px-4 py-1.5 text-sm font-medium hover:bg-muted"
        >
          Primerjaj
        </button>
        <datalist id="kratice">
          {candidates.map((c) => (
            <option key={c.kratica} value={c.kratica}>
              {c.naziv}
            </option>
          ))}
        </datalist>
      </form>

      {a && b && bodyA && bodyB ? (
        <DiffViewer oldValue={bodyA} newValue={bodyB} leftTitle={a} rightTitle={b} />
      ) : a && b ? (
        <p className="text-sm text-muted-foreground">
          {!bodyA ? `Predpis ${a} ni najden.` : `Predpis ${b} ni najden.`}
        </p>
      ) : (
        <p className="text-sm text-muted-foreground">Vnesite obe kratici, da prikaže primerjavo.</p>
      )}
    </main>
  );
}
