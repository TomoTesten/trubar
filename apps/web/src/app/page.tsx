import Link from 'next/link';

const SAMPLES: Array<{ kratica: string; naziv: string }> = [
  { kratica: 'ZKP', naziv: 'Zakon o kazenskem postopku' },
  { kratica: 'ZUP', naziv: 'Zakon o splošnem upravnem postopku' },
  { kratica: 'ZGD-1', naziv: 'Zakon o gospodarskih družbah' },
  { kratica: 'ZDR-1', naziv: 'Zakon o delovnih razmerjih' },
  { kratica: 'ZPP', naziv: 'Zakon o pravdnem postopku' },
  { kratica: 'ZIZ', naziv: 'Zakon o izvršbi in zavarovanju' },
];

export default function Home() {
  return (
    <main className="mx-auto flex max-w-3xl flex-1 flex-col gap-12 px-4 py-16">
      <header className="space-y-4">
        <p className="text-xs uppercase tracking-[0.18em] text-muted-foreground">T.R.U.B.A.R.</p>
        <h1 className="text-4xl font-bold tracking-tight">
          Transparentni register urejenih besedil aktov Republike Slovenije
        </h1>
        <p className="max-w-2xl text-muted-foreground">
          Slovenska zakonodaja kot Git repozitorij. Vsak zakon je Markdown datoteka, vsaka
          sprememba je datiran commit. Repozitorij obsega obdobje od 1946 do danes.
        </p>
      </header>

      <section className="space-y-3">
        <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
          Brskaj
        </h2>
        <ul className="grid gap-2 sm:grid-cols-2">
          {[
            { href: '/zakoni', label: 'Zakoni' },
            { href: '/uredbe', label: 'Uredbe' },
            { href: '/pravilniki', label: 'Pravilniki' },
            { href: '/npb', label: 'Prečiščena besedila (NPB)' },
            { href: '/lokalni', label: 'Lokalni predpisi' },
          ].map(({ href, label }) => (
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
      </section>

      <section className="space-y-3">
        <h2 className="text-sm font-medium uppercase tracking-wider text-muted-foreground">
          Pogosti zakoni
        </h2>
        <ul className="grid gap-2 sm:grid-cols-2">
          {SAMPLES.map(({ kratica, naziv }) => (
            <li key={kratica}>
              <Link
                href={`/${kratica}`}
                className="flex items-baseline gap-3 rounded-md border border-border bg-card px-3 py-2 text-sm hover:bg-muted"
              >
                <span className="font-mono font-semibold">{kratica}</span>
                <span className="text-muted-foreground">{naziv}</span>
              </Link>
            </li>
          ))}
        </ul>
      </section>

      <footer className="mt-auto border-t border-border pt-6 text-xs text-muted-foreground">
        <p>
          Vir besedil:{' '}
          <a
            href="https://www.uradni-list.si/"
            className="underline"
            target="_blank"
            rel="noopener"
          >
            Uradni list RS
          </a>{' '}
          ·{' '}
          <a href="https://pisrs.si/" className="underline" target="_blank" rel="noopener">
            PISRS
          </a>
          . Koda:{' '}
          <a
            href="https://github.com/TomoTesten/trubar"
            className="underline"
            target="_blank"
            rel="noopener"
          >
            GitHub
          </a>
          . Besedila so javna domena (CC0).
        </p>
      </footer>
    </main>
  );
}
