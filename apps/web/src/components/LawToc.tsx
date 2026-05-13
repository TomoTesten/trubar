// Port of build_site.py:146-151 `render_toc`. Hidden when fewer than 5 členi —
// the existing site treats short laws as not needing in-page navigation.

export function LawToc({ cleni }: { cleni: string[] }) {
  if (cleni.length < 5) return null;
  return (
    <nav
      aria-label="Členi"
      className="mb-6 flex flex-wrap items-baseline gap-x-1.5 gap-y-1 border-y border-border py-3 text-sm"
    >
      <strong className="mr-2">Členi:</strong>
      {cleni.map((n) => (
        <a key={n} href={`#clen-${n}`} className="text-muted-foreground hover:text-foreground">
          {n}
        </a>
      ))}
    </nav>
  );
}
