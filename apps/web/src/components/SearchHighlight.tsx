'use client';

// When a law page is opened with ?q=<query>, walk the article body and wrap
// matches in <mark>. Adds a small floating widget showing N matches with
// prev/next navigation. Triggered from the ⌘K palette which navigates with
// ?q= preserved.

import { useEffect, useMemo, useState } from 'react';
import { useSearchParams } from 'next/navigation';

function escapeRegex(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

function highlightAll(root: Element, regex: RegExp): HTMLElement[] {
  const marks: HTMLElement[] = [];
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
    acceptNode(node) {
      const parent = node.parentElement;
      if (!parent) return NodeFilter.FILTER_REJECT;
      const tag = parent.tagName;
      if (tag === 'SCRIPT' || tag === 'STYLE' || tag === 'MARK') return NodeFilter.FILTER_REJECT;
      return node.nodeValue && regex.test(node.nodeValue)
        ? NodeFilter.FILTER_ACCEPT
        : NodeFilter.FILTER_REJECT;
    },
  });

  const toProcess: Text[] = [];
  for (let n = walker.nextNode(); n; n = walker.nextNode()) toProcess.push(n as Text);

  for (const textNode of toProcess) {
    const parts = textNode.nodeValue!.split(regex);
    if (parts.length === 1) continue;
    const frag = document.createDocumentFragment();
    let inMatch = false;
    for (const part of parts) {
      if (!inMatch) {
        if (part) frag.appendChild(document.createTextNode(part));
      } else {
        const mark = document.createElement('mark');
        mark.className =
          'rounded-sm bg-yellow-200 px-0.5 text-foreground dark:bg-yellow-500/40 data-[active=true]:bg-orange-300 data-[active=true]:dark:bg-orange-500/70';
        mark.textContent = part;
        frag.appendChild(mark);
        marks.push(mark);
      }
      inMatch = !inMatch;
    }
    textNode.parentNode!.replaceChild(frag, textNode);
  }
  return marks;
}

export function SearchHighlight() {
  const params = useSearchParams();
  const q = params.get('q') ?? '';
  const [matches, setMatches] = useState<HTMLElement[]>([]);
  const [active, setActive] = useState(0);

  // Build a `(captured) | non-capturing splitter` regex that produces alternating
  // [text, match, text, match, …] when used with String.split.
  const regex = useMemo(() => {
    if (q.trim().length < 2) return null;
    return new RegExp(`(${escapeRegex(q.trim())})`, 'gi');
  }, [q]);

  useEffect(() => {
    if (!regex) {
      setMatches([]);
      return;
    }
    const article = document.querySelector('[data-pagefind-body]');
    if (!article) return;
    const m = highlightAll(article, regex);
    setMatches(m);
    setActive(0);
    // Clean up: unwrap the <mark> elements on unmount or query change.
    return () => {
      for (const mark of m) {
        const parent = mark.parentNode;
        if (!parent) continue;
        while (mark.firstChild) parent.insertBefore(mark.firstChild, mark);
        parent.removeChild(mark);
      }
      // Coalesce adjacent text nodes that the split left behind.
      article.normalize();
    };
  }, [regex]);

  useEffect(() => {
    matches.forEach((m, i) => {
      m.dataset.active = i === active ? 'true' : 'false';
    });
    matches[active]?.scrollIntoView({ behavior: 'smooth', block: 'center' });
  }, [matches, active]);

  if (!regex || matches.length === 0) return null;

  return (
    <div
      role="region"
      aria-label="Iskanje v besedilu"
      className="fixed bottom-4 right-4 z-40 flex items-center gap-2 rounded-full border border-border bg-background/95 px-3 py-1.5 text-xs shadow-md backdrop-blur"
    >
      <span className="font-mono">
        {active + 1} / {matches.length}
      </span>
      <button
        type="button"
        aria-label="Prejšnji zadetek"
        onClick={() => setActive((i) => (i - 1 + matches.length) % matches.length)}
        className="rounded p-1 hover:bg-muted"
      >
        ↑
      </button>
      <button
        type="button"
        aria-label="Naslednji zadetek"
        onClick={() => setActive((i) => (i + 1) % matches.length)}
        className="rounded p-1 hover:bg-muted"
      >
        ↓
      </button>
    </div>
  );
}
