'use client';

// Virtualized table for category listings. Client island: filter input + arrow
// navigation; rendering uses @tanstack/react-virtual so only the visible rows
// land in the DOM (handles 10k+ entries on a single page without jank).

import { useMemo, useRef, useState, type ReactNode } from 'react';
import Link from 'next/link';
import { useVirtualizer } from '@tanstack/react-virtual';
import type { ManifestEntry } from '@/lib/laws';

const ROW_HEIGHT = 44; // px

// Picks between Next's <Link> for internal routes (prefetch, client nav) and a
// plain <a target=_blank> for external Uradni list URLs (občinski entries).
function ListingLink({
  href,
  external,
  className,
  children,
}: {
  href: string;
  external: boolean;
  className?: string;
  children: ReactNode;
}) {
  if (external) {
    return (
      <a href={href} target="_blank" rel="noopener" className={className}>
        {children}
      </a>
    );
  }
  return (
    <Link href={href} className={className}>
      {children}
    </Link>
  );
}

type Props = {
  entries: ManifestEntry[];
  // String prefix prepended to kratica for the row URL (e.g. "/" for laws,
  // "/npb/" for NPB). Functions can't cross the RSC→client boundary, so the
  // server-side caller serializes the URL shape into a prefix string.
  urlPrefix: string;
  // When true, rows link to entry.vir (external source URL) and open in a new
  // tab — used for občinski entries which don't have detail pages.
  externalLink?: boolean;
};

function normalize(s: string): string {
  return s
    .toLowerCase()
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '');
}

export function LawListingTable({ entries, urlPrefix, externalLink = false }: Props) {
  const [q, setQ] = useState('');
  const filtered = useMemo(() => {
    if (!q.trim()) return entries;
    const needle = normalize(q.trim());
    return entries.filter((e) => {
      const k = normalize(e.kratica);
      const n = normalize(e.naziv);
      return k.includes(needle) || n.includes(needle);
    });
  }, [entries, q]);

  const parentRef = useRef<HTMLDivElement>(null);
  const virtualizer = useVirtualizer({
    count: filtered.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => ROW_HEIGHT,
    overscan: 10,
  });

  return (
    <div className="space-y-3">
      <div className="flex flex-wrap items-baseline justify-between gap-2">
        <input
          type="search"
          placeholder="Filtriraj po kratici ali nazivu…"
          value={q}
          onChange={(e) => setQ(e.target.value)}
          className="min-w-[260px] flex-1 rounded-md border border-border bg-background px-3 py-2 text-sm"
        />
        <span className="text-xs text-muted-foreground">
          {filtered.length === entries.length
            ? `${entries.length.toLocaleString('sl-SI')} zadetkov`
            : `${filtered.length.toLocaleString('sl-SI')} od ${entries.length.toLocaleString('sl-SI')}`}
        </span>
      </div>

      <div
        ref={parentRef}
        className="h-[calc(100vh-260px)] min-h-[400px] overflow-auto rounded-md border border-border"
      >
        <div
          style={{ height: virtualizer.getTotalSize(), position: 'relative' }}
          className="w-full"
        >
          {virtualizer.getVirtualItems().map((vrow) => {
            const e = filtered[vrow.index];
            return (
              <div
                key={`${e.kratica}-${vrow.index}`}
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  right: 0,
                  transform: `translateY(${vrow.start}px)`,
                  height: vrow.size,
                }}
                className="border-b border-border last:border-b-0"
              >
                <ListingLink
                  href={externalLink ? (e.vir ?? `${urlPrefix}${e.kratica}`) : `${urlPrefix}${e.kratica}`}
                  external={externalLink && !!e.vir}
                  className="flex h-full items-center gap-4 px-4 text-sm hover:bg-muted"
                >
                  <span className="w-32 shrink-0 truncate font-mono text-xs font-semibold">
                    {e.kratica}
                  </span>
                  <span className="flex-1 truncate">{e.naziv}</span>
                  {e.datum ? (
                    <span className="hidden w-24 shrink-0 text-right font-mono text-xs text-muted-foreground md:inline">
                      {e.datum}
                    </span>
                  ) : null}
                </ListingLink>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
