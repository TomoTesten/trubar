import { getLawManifest, type ManifestEntry } from '@/lib/laws';
import { LawListingTable } from './LawListingTable';

type Props = {
  title: string;
  description: string;
  /** vrsta value(s) to include in this listing. */
  vrsta: string | readonly string[];
  /** URL prefix for row links (e.g. '/' or '/npb/'). Ignored when externalLink=true. */
  urlPrefix?: string;
  /** When true, rows link to entry.vir in a new tab (občinski entries have no detail pages). */
  externalLink?: boolean;
};

export async function CategoryPage({
  title,
  description,
  vrsta,
  urlPrefix = '/',
  externalLink = false,
}: Props) {
  const wanted = typeof vrsta === 'string' ? [vrsta] : vrsta;
  const manifest = await getLawManifest();
  const entries: ManifestEntry[] = manifest
    .filter((e) => e.vrsta && wanted.includes(e.vrsta))
    .sort((a, b) => a.naziv.localeCompare(b.naziv, 'sl'));

  return (
    <main className="mx-auto max-w-6xl px-4 py-8">
      <header className="mb-6">
        <h1 className="text-2xl font-semibold tracking-tight">{title}</h1>
        <p className="mt-1 text-sm text-muted-foreground">{description}</p>
      </header>
      <LawListingTable entries={entries} urlPrefix={urlPrefix} externalLink={externalLink} />
    </main>
  );
}
