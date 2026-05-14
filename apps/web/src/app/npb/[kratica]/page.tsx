import type { Metadata } from 'next';
import Link from 'next/link';
import { Suspense } from 'react';
import { notFound } from 'next/navigation';
import { getLawManifest, loadNpb } from '@/lib/laws';
import { LawSidebar } from '@/components/LawSidebar';
import { LawToc } from '@/components/LawToc';
import { AmendmentList } from '@/components/AmendmentList';
import { CourtDecisions } from '@/components/CourtDecisions';
import { AiPanel } from '@/components/AiPanel';
import { SearchHighlight } from '@/components/SearchHighlight';

export const dynamicParams = true;

// Same SSG_FULL gate as /[kratica]: production pre-renders all ~10,042 NPB
// pages; dev caps at 25 for fast iteration.
const FULL = process.env.SSG_FULL === '1';
const DEV_CAP = 25;

export async function generateStaticParams() {
  const manifest = await getLawManifest();
  const npb = manifest.filter((m) => m.vrsta === 'NPB');
  const set = FULL ? npb : npb.slice(0, DEV_CAP);
  return set.map((m) => ({ kratica: m.kratica }));
}

async function tryLoad(kratica: string) {
  const manifest = await getLawManifest();
  const entry = manifest.find((m) => m.kratica === kratica && m.vrsta === 'NPB');
  if (!entry) return null;
  return loadNpb(kratica);
}

export async function generateMetadata(
  props: PageProps<'/npb/[kratica]'>,
): Promise<Metadata> {
  const { kratica } = await props.params;
  const law = await tryLoad(kratica);
  if (!law) return {};
  return {
    title: `${law.frontmatter.kratica} — ${law.frontmatter.naziv}`,
    description: law.frontmatter.naziv,
  };
}

export default async function Page(props: PageProps<'/npb/[kratica]'>) {
  const { kratica } = await props.params;
  const law = await tryLoad(kratica);
  if (!law) notFound();
  const { frontmatter, html, cleni } = law;

  return (
    <main className="mx-auto max-w-7xl px-4 py-6">
      <header className="mb-6">
        <nav className="text-sm">
          <Link href="/npb" className="text-muted-foreground hover:text-foreground">
            ← Prečiščena besedila
          </Link>
        </nav>
        <h1 className="mt-3 text-3xl font-bold tracking-tight">{frontmatter.naziv}</h1>
      </header>

      <div className="grid gap-8 md:grid-cols-[260px_1fr]">
        <LawSidebar frontmatter={frontmatter} isNpb />

        <article
          data-pagefind-body
          data-pagefind-meta={`kratica:${frontmatter.kratica},vrsta:NPB`}
        >
          <LawToc cleni={cleni} />
          <div
            className="prose prose-sm max-w-none dark:prose-invert"
            dangerouslySetInnerHTML={{ __html: html }}
          />
          <AmendmentList frontmatter={frontmatter} isNpb />
          <CourtDecisions kratica={frontmatter.kratica} />
        </article>
      </div>

      <AiPanel lawName={frontmatter.naziv} />
      <Suspense fallback={null}>
        <SearchHighlight />
      </Suspense>
    </main>
  );
}
