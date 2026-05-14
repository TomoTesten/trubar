'use client';

// Persistent top bar: brand link + ⌘K search trigger. Stays as a single
// client island in the root layout so the shortcut works on every page.

import Link from 'next/link';
import { useEffect, useState } from 'react';
import { SearchCommand } from './SearchCommand';

export function NavBar() {
  const [shortcut, setShortcut] = useState('Ctrl K');

  // Show the platform-correct shortcut hint after mount (avoid hydration mismatch).
  useEffect(() => {
    if (typeof navigator !== 'undefined' && /Mac|iPad|iPhone/i.test(navigator.platform)) {
      setShortcut('⌘ K');
    }
  }, []);

  function openSearch() {
    window.dispatchEvent(new KeyboardEvent('keydown', { key: 'k', metaKey: true }));
  }

  return (
    <>
      <header className="sticky top-0 z-30 border-b border-border bg-background/80 backdrop-blur">
        <div className="mx-auto flex h-12 max-w-7xl items-center justify-between px-4">
          <Link href="/" className="text-sm font-semibold tracking-tight">
            T.R.U.B.A.R.
          </Link>
          <button
            type="button"
            onClick={openSearch}
            className="inline-flex items-center gap-2 rounded-md border border-border bg-card px-3 py-1 text-xs text-muted-foreground hover:bg-muted"
            aria-label="Odpri iskanje"
          >
            <span>Išči predpise…</span>
            <kbd className="font-mono text-[10px] tracking-wider text-foreground/70">
              {shortcut}
            </kbd>
          </button>
        </div>
      </header>
      <SearchCommand />
    </>
  );
}
