import type { Metadata } from 'next';
import Link from 'next/link';
import { Suspense } from 'react';
import { notFound } from 'next/navigation';
import { getLawManifest, loadLaw, RENDERABLE_VRSTE } from '@/lib/laws';
import { LawSidebar } from '@/components/LawSidebar';
import { LawToc } from '@/components/LawToc';
import { AmendmentList } from '@/components/AmendmentList';
import { DatePicker } from '@/components/DatePicker';
import { CourtDecisions } from '@/components/CourtDecisions';
import { AiPanel } from '@/components/AiPanel';
import { SearchHighlight } from '@/components/SearchHighlight';

export const dynamicParams = true;

// SSG_FULL=1 (set on Vercel Production) pre-renders all ~3,975 Sprejet zakon
// for instant first-hit performance. Dev/preview builds keep a 25-page cap for
// fast iteration; the long tail still renders via ISR on first hit either way.
const FULL = process.env.SSG_FULL === '1';
const DEV_CAP = 25;

export async function generateStaticParams() {
  const manifest = await getLawManifest();
  const zakoni = manifest.filter((m) => m.vrsta === 'Sprejet zakon');
  const set = FULL ? zakoni : zakoni.slice(0, DEV_CAP);
  return set.map((m) => ({ kratica: m.kratica }));
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
  const { frontmatter, html, cleni, versions } = law;

  return (
    <main className="mx-auto max-w-7xl px-4 py-6">
      <header className="mb-6">
        <nav className="text-sm">
          <Link href="/" className="text-muted-foreground hover:text-foreground">
            ← T.R.U.B.A.R.
          </Link>
        </nav>
        <h1 className="mt-3 text-3xl font-bold tracking-tight">{frontmatter.naziv}</h1>
      </header>

      <div className="grid gap-8 md:grid-cols-[260px_1fr]">
        <div className="space-y-6">
          <LawSidebar frontmatter={frontmatter} />
          {versions.length > 1 ? <DatePicker versions={versions} /> : null}
        </div>

        <article
          data-pagefind-body
          data-pagefind-meta={`kratica:${frontmatter.kratica}${
            frontmatter.vrsta ? `,vrsta:${frontmatter.vrsta}` : ''
          }${frontmatter.organ ? `,organ:${frontmatter.organ}` : ''}${
            frontmatter.status ? `,status:${frontmatter.status}` : ''
          }${frontmatter.datum ? `,year:${frontmatter.datum.slice(0, 4)}` : ''}`}
        >
          <LawToc cleni={cleni} />
          <div
            className="prose prose-sm max-w-none dark:prose-invert"
            dangerouslySetInnerHTML={{ __html: html }}
          />
          <AmendmentList frontmatter={frontmatter} isNpb={false} />
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
