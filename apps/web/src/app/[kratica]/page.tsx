import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getLawManifest, loadLaw, RENDERABLE_VRSTE } from '@/lib/laws';

export const dynamicParams = true;

// SSG cap: in dev/preview we only pre-render a small set so iteration is fast.
// Production cutover bumps this to the full ~3,975 zakoni (and adds NPB at /npb/).
const SSG_LIMIT = process.env.SSG_LIMIT ? Number(process.env.SSG_LIMIT) : 25;

export async function generateStaticParams() {
  const manifest = await getLawManifest();
  return manifest
    .filter((m) => m.vrsta === 'Sprejet zakon')
    .slice(0, SSG_LIMIT)
    .map((m) => ({ kratica: m.kratica }));
}

async function tryLoad(kratica: string) {
  const manifest = await getLawManifest();
  const entry = manifest.find((m) => m.kratica === kratica);
  if (!entry || !entry.vrsta || !RENDERABLE_VRSTE.has(entry.vrsta)) return null;
  return loadLaw(kratica);
}

export async function generateMetadata(props: PageProps<'/[kratica]'>): Promise<Metadata> {
  const { kratica } = await props.params;
  const law = await tryLoad(kratica);
  if (!law) return {};
  return {
    title: `${law.frontmatter.kratica} — ${law.frontmatter.naziv}`,
    description: law.frontmatter.naziv,
  };
}

export default async function LawPage(props: PageProps<'/[kratica]'>) {
  const { kratica } = await props.params;
  const law = await tryLoad(kratica);
  if (!law) notFound();
  const { frontmatter, html } = law;

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <header className="mb-8 border-b pb-6">
        <p className="text-sm text-muted-foreground">{frontmatter.kratica}</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight">{frontmatter.naziv}</h1>
        {frontmatter.datum ? (
          <p className="mt-2 text-sm text-muted-foreground">Sprejet: {frontmatter.datum}</p>
        ) : null}
      </header>

      <article
        className="prose prose-sm max-w-none dark:prose-invert"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </main>
  );
}
