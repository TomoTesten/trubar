import type { Root, Text } from 'mdast';
import type { Node, Parent } from 'unist';
import { visit, SKIP } from 'unist-util-visit';

type Options = {
  /** Map of kratica → URL slug, used to resolve cross-links. */
  index: Map<string, string>;
  /** Current page's kratica — skipped to avoid self-links. */
  current: string;
};

const LOOKBEHIND = /[A-Za-zÀ-žčšžČŠŽ0-9-]/;

// Port of build_site.py:71-88 `inject_crosslinks`. Walks MDAST text nodes (not
// link/code/inlineCode contents) and splits each into [text, link, text, ...]
// children when it finds known kratice as standalone tokens. Longest match first
// so "ZKP-A" wins over "ZKP".
export function remarkKraticaLinks({ index, current }: Options) {
  const kratice = [...index.keys()].filter((k) => k && k !== current).sort((a, b) => b.length - a.length);
  if (kratice.length === 0) return () => {};

  const pattern = new RegExp(
    `(?<![A-Za-zÀ-žčšžČŠŽ0-9-])(${kratice.map(escapeRegex).join('|')})(?![A-Za-zÀ-žčšžČŠŽ0-9-])`,
    'g',
  );

  return (tree: Root) => {
    visit(tree, 'text', (node: Text, indexInParent, parent: Parent | undefined) => {
      if (!parent || indexInParent == null) return;
      if (parent.type === 'link' || parent.type === 'linkReference') return;
      if (parent.type === 'code' || parent.type === 'inlineCode') return;

      const text = node.value;
      pattern.lastIndex = 0;
      // Boundary check: pattern already enforces no surrounding word-char, but
      // JS regex lookbehind/lookahead handles that — we only need to scan.
      if (!pattern.test(text)) return;

      pattern.lastIndex = 0;
      const children: Node[] = [];
      let last = 0;
      let m: RegExpExecArray | null;
      while ((m = pattern.exec(text)) !== null) {
        const k = m[1];
        const slug = index.get(k);
        if (!slug || slug === current) continue;
        if (m.index > last) children.push({ type: 'text', value: text.slice(last, m.index) } as Text);
        children.push({
          type: 'link',
          url: `/${slug}`,
          title: k,
          data: { hProperties: { className: ['law-ref'] } },
          children: [{ type: 'text', value: k } as Text],
        } as unknown as Node);
        last = m.index + k.length;
      }
      if (children.length === 0) return;
      if (last < text.length) children.push({ type: 'text', value: text.slice(last) } as Text);

      parent.children.splice(indexInParent, 1, ...(children as Parent['children']));
      return [SKIP, indexInParent + children.length];
    });
  };
}

function escapeRegex(s: string): string {
  return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}
