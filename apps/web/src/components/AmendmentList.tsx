import type { LawFrontmatter } from '@/lib/laws';

const GH_BLOB = 'https://github.com/TomoTesten/trubar/blob/master';
const GH_COMMITS = 'https://github.com/TomoTesten/trubar/commits/master';

// Port of build_site.py:233-253 amendment list. Each entry links to the amendment
// law page in our site, plus a side link to its source MD on GitHub. The header
// gets a "git ↗" deep-link to the full file history.

export function AmendmentList({
  frontmatter,
  isNpb,
}: {
  frontmatter: LawFrontmatter;
  isNpb: boolean;
}) {
  const items = frontmatter.spremembe;
  if (!items || items.length === 0) return null;
  const subdir = isNpb ? 'si/npb' : 'si';
  const historyUrl = `${GH_COMMITS}/${subdir}/${frontmatter.kratica}.md`;

  return (
    <section className="mt-8 border-t border-border pt-6">
      <h2 className="mb-3 text-lg font-semibold">
        Kronologija sprememb{' '}
        <a
          href={historyUrl}
          target="_blank"
          rel="noopener"
          className="ml-1 align-middle text-sm font-normal text-muted-foreground underline"
          title="Celotna git zgodovina"
        >
          git ↗
        </a>
      </h2>
      <ul className="space-y-1.5 text-sm">
        {items.map((a) => (
          <li key={a.kratica} className="flex flex-wrap items-baseline gap-x-2">
            <span className="font-mono text-xs text-muted-foreground">{a.datum ?? ''}</span>
            <a href={`/${a.kratica}`} className="font-medium underline">
              {a.kratica}
            </a>
            <span className="text-muted-foreground">— {a.naziv ?? a.kratica}</span>
            <a
              href={`${GH_BLOB}/si/${a.kratica}.md`}
              target="_blank"
              rel="noopener"
              className="text-xs text-muted-foreground underline"
              title="Besedilo spremembe na GitHubu"
            >
              diff ↗
            </a>
          </li>
        ))}
      </ul>
    </section>
  );
}
