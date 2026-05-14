'use client';

// Global ⌘K command palette. Client island: keyboard shortcut + dynamic
// Pagefind import + debounced query. The index lives at /_pagefind and is
// generated from docs/ at build time (see scripts/build-pagefind.mjs).

import { useCallback, useEffect, useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from '@/components/ui/command';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

type PagefindMeta = { kratica?: string; vrsta?: string; title?: string };
type PagefindResultData = {
  url: string;
  excerpt: string;
  meta: PagefindMeta;
};
type PagefindResult = { id: string; data: () => Promise<PagefindResultData> };
type PagefindApi = {
  options(opts: { baseUrl?: string }): Promise<void>;
  search(query: string): Promise<{ results: PagefindResult[] }>;
};

// Convert Pagefind's docs/-style URLs back to the new app's slug routes:
// /trubar/si/ZKP/  → /ZKP
// /trubar/npb/ANJP299/ → /npb/ANJP299
function normalizeUrl(url: string): string {
  return url
    .replace(/^\/trubar\//, '/')
    .replace(/^\/si\//, '/')
    .replace(/\/$/, '');
}

export function SearchCommand() {
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState('');
  const [results, setResults] = useState<PagefindResultData[]>([]);
  const [loading, setLoading] = useState(false);
  const pagefindRef = useRef<PagefindApi | null>(null);
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const router = useRouter();

  // ⌘K / Ctrl+K binding.
  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'k' && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((v) => !v);
      }
    };
    window.addEventListener('keydown', onKey);
    return () => window.removeEventListener('keydown', onKey);
  }, []);

  // Lazy-load Pagefind on first open so the 280 KB UI bundle doesn't ship to
  // every visitor up front.
  const ensurePagefind = useCallback(async (): Promise<PagefindApi | null> => {
    if (pagefindRef.current) return pagefindRef.current;
    try {
      // Runtime URL — bundler must not resolve it. TS doesn't know about /_pagefind.
      const importPath = '/_pagefind/pagefind.js';
      const mod = (await import(/* webpackIgnore: true */ /* @vite-ignore */ importPath)) as unknown as PagefindApi;
      await mod.options({ baseUrl: '/' });
      pagefindRef.current = mod;
      return mod;
    } catch (err) {
      console.warn('[search] failed to load Pagefind index:', err);
      return null;
    }
  }, []);

  // Debounced search; cancels in-flight searches when the query changes.
  useEffect(() => {
    if (debounceRef.current) clearTimeout(debounceRef.current);
    if (!open || query.trim().length < 2) {
      setResults([]);
      return;
    }
    debounceRef.current = setTimeout(async () => {
      const pf = await ensurePagefind();
      if (!pf) return;
      setLoading(true);
      try {
        const res = await pf.search(query.trim());
        const top = await Promise.all(res.results.slice(0, 10).map((r) => r.data()));
        setResults(top);
      } finally {
        setLoading(false);
      }
    }, 180);
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current);
    };
  }, [query, open, ensurePagefind]);

  const onSelect = useCallback(
    (url: string) => {
      setOpen(false);
      // Carry the query through so the law page can highlight in-page matches.
      const q = query.trim();
      router.push(q ? `${url}?q=${encodeURIComponent(q)}` : url);
    },
    [router, query],
  );

  return (
    <Dialog open={open} onOpenChange={setOpen}>
      <DialogHeader className="sr-only">
        <DialogTitle>Iskanje</DialogTitle>
        <DialogDescription>Iskanje po slovenski zakonodaji</DialogDescription>
      </DialogHeader>
      <DialogContent
        showCloseButton={false}
        className="top-1/3 translate-y-0 overflow-hidden rounded-xl! p-0"
      >
        <Command shouldFilter={false} className="rounded-none border-0">
          <CommandInput
            value={query}
            onValueChange={setQuery}
            placeholder="Poiščite predpis ali besedo iz besedila…"
          />
          <CommandList>
        {query.trim().length < 2 ? (
          <CommandEmpty>Vpišite vsaj 2 znaka.</CommandEmpty>
        ) : loading && results.length === 0 ? (
          <CommandEmpty>Iskanje…</CommandEmpty>
        ) : results.length === 0 ? (
          <CommandEmpty>Ni zadetkov.</CommandEmpty>
        ) : (
          <CommandGroup heading={`Zadetki (${results.length})`}>
            {results.map((r) => {
              const url = normalizeUrl(r.url);
              const kratica = r.meta.kratica ?? url.replace(/^\//, '');
              const title = r.meta.title ?? '';
              return (
                <CommandItem
                  key={url}
                  value={url}
                  onSelect={() => onSelect(url)}
                  className="flex flex-col items-start gap-1"
                >
                  <div className="flex items-baseline gap-2 text-sm">
                    <span className="font-mono font-semibold">{kratica}</span>
                    {r.meta.vrsta ? (
                      <span className="text-xs text-muted-foreground">{r.meta.vrsta}</span>
                    ) : null}
                  </div>
                  {title ? (
                    <span className="line-clamp-1 text-xs text-muted-foreground">{title}</span>
                  ) : null}
                  <span
                    className="line-clamp-2 text-xs text-muted-foreground/80"
                    dangerouslySetInnerHTML={{ __html: r.excerpt }}
                  />
                </CommandItem>
              );
            })}
          </CommandGroup>
        )}
          </CommandList>
        </Command>
      </DialogContent>
    </Dialog>
  );
}
