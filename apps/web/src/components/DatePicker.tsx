'use client';

// Client island: <input type="date"> + URL param wiring. Versions are
// frozen at build time, so this is interactive only — no data fetching.

import { useEffect, useState } from 'react';
import type { LawVersion } from '@/lib/laws';

function findVersion(versions: LawVersion[], date: string): LawVersion | null {
  let found: LawVersion | null = null;
  for (const v of versions) {
    if (v.date && v.date <= date) found = v;
    else if (v.date) break;
  }
  return found;
}

export function DatePicker({ versions }: { versions: LawVersion[] }) {
  const [date, setDate] = useState('');

  // Honor ?date= query param on mount (kept from the original Python build).
  useEffect(() => {
    const param = new URLSearchParams(window.location.search).get('date');
    if (param) setDate(param);
  }, []);

  const v = date ? findVersion(versions, date) : null;

  return (
    <div className="space-y-2 rounded-md border border-border bg-card p-3 text-sm">
      <label htmlFor="law-date" className="block font-medium">
        Stanje na datum:
      </label>
      <input
        id="law-date"
        type="date"
        min="1991-01-01"
        value={date}
        onChange={(e) => setDate(e.target.value)}
        className="w-full rounded border border-border bg-background px-2 py-1"
      />
      {date && !v ? (
        <p className="text-xs text-muted-foreground">Zakon na ta datum še ni obstajal.</p>
      ) : null}
      {date && v ? (
        <p className="text-xs text-muted-foreground">
          Na dan <strong className="text-foreground">{date}</strong> je veljala verzija:
          <br />
          <a href={v.url} className="font-medium underline">
            {v.kratica}
          </a>{' '}
          (od {v.date})
        </p>
      ) : null}
    </div>
  );
}
