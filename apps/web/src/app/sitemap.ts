import type { MetadataRoute } from 'next';
import { getLawManifest, RENDERABLE_VRSTE } from '@/lib/laws';

const BASE = process.env.NEXT_PUBLIC_SITE_URL ?? 'https://trubar.vercel.app';

// Single sitemap covering home + listings + all renderable + NPB. Občinski
// entries are intentionally omitted (no detail pages).
//
// Note: total entries (~54k) exceed sitemaps.org's 50k-per-file *recommendation*
// but stay under the hard 50 MB uncompressed cap (~8 MB here). Major engines
// accept this. Splitting into a sitemap index pointing at /sitemap/N.xml chunks
// is a Phase 4 cleanup if we ever see a search engine actually reject.

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const manifest = await getLawManifest();

  const staticRoutes: MetadataRoute.Sitemap = [
    '',
    '/zakoni',
    '/uredbe',
    '/pravilniki',
    '/npb',
    '/lokalni',
    '/primerjaj',
  ].map((p) => ({
    url: `${BASE}${p}`,
    changeFrequency: 'daily',
    priority: p === '' ? 1.0 : 0.6,
  }));

  const lawRoutes: MetadataRoute.Sitemap = [];
  for (const e of manifest) {
    if (e.vrsta === 'NPB') {
      lawRoutes.push({
        url: `${BASE}/npb/${e.kratica}`,
        lastModified: e.datum,
        changeFrequency: 'monthly',
        priority: 0.5,
      });
    } else if (e.vrsta && RENDERABLE_VRSTE.has(e.vrsta)) {
      lawRoutes.push({
        url: `${BASE}/${e.kratica}`,
        lastModified: e.datum,
        changeFrequency: 'monthly',
        priority: e.vrsta === 'Sprejet zakon' ? 0.8 : 0.5,
      });
    }
  }

  return [...staticRoutes, ...lawRoutes];
}
