import type { LawFrontmatter } from '@/lib/laws';
import { StatusBadge } from './StatusBadge';
import { PrintButton } from './PrintButton';

const GH_BLOB = 'https://github.com/TomoTesten/trubar/blob/master';

const BTN =
  'inline-flex items-center gap-2 rounded-md border border-border bg-card px-3 py-1.5 text-sm font-medium text-foreground hover:bg-muted';

type Props = {
  frontmatter: LawFrontmatter;
  isNpb?: boolean;
};

export function LawSidebar({ frontmatter, isNpb = false }: Props) {
  const datum = frontmatter.datum ?? frontmatter.veljaOd ?? '';
  const subdir = isNpb ? 'si/npb' : 'si';

  return (
    <aside className="space-y-6">
      <dl className="grid grid-cols-[max-content_1fr] gap-x-3 gap-y-1.5 text-sm">
        <dt className="text-muted-foreground">Kratica</dt>
        <dd className="font-medium">{frontmatter.kratica}</dd>

        <dt className="text-muted-foreground">Vrsta</dt>
        <dd>{isNpb ? 'Prečiščeno besedilo (NPB)' : (frontmatter.vrsta ?? '')}</dd>

        {!isNpb && frontmatter.status ? (
          <>
            <dt className="text-muted-foreground">Status</dt>
            <dd>
              <StatusBadge status={frontmatter.status} />
            </dd>
          </>
        ) : null}

        {datum ? (
          <>
            <dt className="text-muted-foreground">Datum</dt>
            <dd>{datum}</dd>
          </>
        ) : null}

        {frontmatter.organ ? (
          <>
            <dt className="text-muted-foreground">Organ</dt>
            <dd>{frontmatter.organ}</dd>
          </>
        ) : null}

        {frontmatter.npb ? (
          <>
            <dt className="text-muted-foreground">NPB</dt>
            <dd>{frontmatter.npb}</dd>
          </>
        ) : null}

        {frontmatter.vir ? (
          <>
            <dt className="text-muted-foreground">Vir</dt>
            <dd>
              <a href={frontmatter.vir} target="_blank" rel="noopener" className="underline">
                {isNpb ? 'PISRS' : 'Uradni list RS'}
              </a>
            </dd>
          </>
        ) : null}
      </dl>

      <div className="flex flex-wrap gap-2">
        <PrintButton className={BTN} />
        <a href={`/primerjaj?a=${encodeURIComponent(frontmatter.kratica)}`} className={BTN}>
          ⇄ Primerjaj
        </a>
        <a
          href={`${GH_BLOB}/${subdir}/${frontmatter.kratica}.md`}
          target="_blank"
          rel="noopener"
          className={BTN}
        >
          GitHub ↗
        </a>
      </div>
    </aside>
  );
}
