import Link from 'next/link';

const CATEGORIES = [
  { href: '/zakoni', label: 'Zakoni' },
  { href: '/uredbe', label: 'Uredbe' },
  { href: '/pravilniki', label: 'Pravilniki' },
  { href: '/npb', label: 'Prečiščena besedila' },
  { href: '/lokalni', label: 'Lokalni predpisi' },
];

export default function NotFound() {
  return (
    <main className="mx-auto flex max-w-3xl flex-1 flex-col gap-10 px-4 py-20">
      <header className="space-y-3">
        <p className="font-mono text-sm text-muted-foreground">404</p>
        <h1 className="text-3xl font-bold tracking-tight">Predpis ni najden</h1>
        <p className="text-muted-foreground">
          Iskane strani ni ali pa kratica ni v zbirki. Poiščite predpis z iskalnikom (
          <kbd className="rounded border border-border bg-card px-1.5 py-0.5 font-mono text-[10px]">⌘ K</kbd>
          ) ali brskajte po kategorijah.
        </p>
      </header>

      <nav>
        <h2 className="mb-3 text-sm font-medium uppercase tracking-wider text-muted-foreground">
          Brskaj
        </h2>
        <ul className="grid gap-2 sm:grid-cols-2">
          {CATEGORIES.map(({ href, label }) => (
            <li key={href}>
              <Link
                href={href}
                className="flex items-baseline gap-3 rounded-md border border-border bg-card px-3 py-2 text-sm hover:bg-muted"
              >
                <span className="font-medium">{label}</span>
                <span className="ml-auto text-muted-foreground">→</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </main>
  );
}
