import type { Heading, Root, Text } from 'mdast';
import { visit } from 'unist-util-visit';

// Port of build_site.py:134-144 `add_article_anchors`. Detects "N. člen" headings
// and tags them with id="člen-N" so the TOC and in-page anchors can link to them.
// Collects the člen numbers into the caller-supplied array, in document order.

const CLEN_RE = /^(\d+)\.\s+člen\b/;

export function remarkClenAnchors(collector: string[]) {
  return (tree: Root) => {
    visit(tree, 'heading', (node: Heading) => {
      const first = node.children[0];
      if (!first || first.type !== 'text') return;
      const m = (first as Text).value.match(CLEN_RE);
      if (!m) return;
      const num = m[1];
      collector.push(num);
      // Attach id via mdast→hast data channel.
      const data = (node.data ??= {});
      const hProperties = ((data as { hProperties?: Record<string, unknown> }).hProperties ??= {});
      (hProperties as Record<string, unknown>).id = `clen-${num}`;
    });
  };
}
