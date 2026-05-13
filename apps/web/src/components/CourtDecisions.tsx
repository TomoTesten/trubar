'use client';

// Client island: court decisions are fetched lazily via IntersectionObserver.
// The shards (/data/courts/<kratica>.json) are static assets; 404 is silent.

import { useEffect, useRef, useState } from 'react';

type Decision = {
  id?: string;
  datum?: string;
  zbirka?: string;
  vir?: string;
};

function shortZbirka(z: string | undefined): string {
  if (!z) return '';
  return z.replace('Sodna praksa ', '').replace(' sodišča', '');
}

export function CourtDecisions({ kratica }: { kratica: string }) {
  const ref = useRef<HTMLDivElement>(null);
  const [items, setItems] = useState<Decision[] | null>(null);

  useEffect(() => {
    if (!ref.current) return;
    const el = ref.current;
    const load = async () => {
      try {
        const r = await fetch(`/data/courts/${encodeURIComponent(kratica)}.json`);
        if (!r.ok) return;
        const data = (await r.json()) as Decision[];
        if (Array.isArray(data) && data.length > 0) setItems(data);
      } catch {
        // 404 / network — silent, matching the original site's behavior.
      }
    };
    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver(
        (entries) => {
          if (entries[0]?.isIntersecting) {
            obs.disconnect();
            void load();
          }
        },
        { rootMargin: '200px' },
      );
      obs.observe(el);
      return () => obs.disconnect();
    }
    void load();
  }, [kratica]);

  if (!items) return <div ref={ref} aria-hidden />;

  return (
    <section ref={ref} className="mt-8 border-t border-border pt-6">
      <h2 className="mb-3 text-lg font-semibold">Sodna praksa</h2>
      <ul className="space-y-1 text-sm">
        {items.map((d, i) => {
          const label = d.datum ? d.datum.slice(0, 10) : (d.id ?? '');
          const z = shortZbirka(d.zbirka);
          return (
            <li key={`${d.id ?? label}-${i}`}>
              {d.vir ? (
                <a href={d.vir} target="_blank" rel="noopener" className="underline">
                  {label}
                  {z ? ` (${z})` : ''}
                </a>
              ) : (
                <span>
                  {label}
                  {z ? ` (${z})` : ''}
                </span>
              )}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
