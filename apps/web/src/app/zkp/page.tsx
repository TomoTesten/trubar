import type { Metadata } from 'next';
import { loadLaw, formatLawDate } from '@/lib/laws';

export async function generateMetadata(): Promise<Metadata> {
  const { frontmatter } = await loadLaw('ZKP');
  return {
    title: `${frontmatter.kratica} — ${frontmatter.naziv}`,
    description: frontmatter.naziv,
  };
}

export default async function ZkpPage() {
  const { frontmatter, html } = await loadLaw('ZKP');
  const sprejet = formatLawDate(frontmatter.datum);

  return (
    <main className="mx-auto max-w-3xl px-4 py-8">
      <header className="mb-8 border-b pb-6">
        <p className="text-sm text-muted-foreground">{frontmatter.kratica}</p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight">{frontmatter.naziv}</h1>
        {sprejet ? (
          <p className="mt-2 text-sm text-muted-foreground">Sprejet: {sprejet}</p>
        ) : null}
      </header>

      <article
        className="prose prose-sm max-w-none dark:prose-invert"
        dangerouslySetInnerHTML={{ __html: html }}
      />
    </main>
  );
}
