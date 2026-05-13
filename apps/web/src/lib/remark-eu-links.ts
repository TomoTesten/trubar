import type { Root, Text } from 'mdast';
import type { Node, Parent } from 'unist';
import { visit, SKIP } from 'unist-util-visit';

// Port of build_site.py:94-120 `inject_eu_links`. Detects four reference shapes:
//   Direktiva YYYY/NNN/(ES|EU|EGS|Euratom)         → CELEX 3{YYYY}L{NNN:04d}
//   Odločba   YYYY/NNN/(ES|EU|EGS)                 → CELEX 3{YYYY}D{NNN:04d}
//   Sklep     YYYY/NNN/(EU|ES|EGS)                 → CELEX 3{YYYY}D{NNN:04d}
//   Uredba (EU|ES|EGS|Euratom) [št.] NNN/YYYY      → CELEX 3{YYYY}R{NNN:04d}
//
// Fixes two bugs from the original Python:
//  - Uredba syntax is NNN/YYYY (number first), not YYYY/NNN — the Python labelled
//    them swapped, producing wrong CELEX codes (e.g. 31024R2013 for "1024/2013"
//    instead of the correct 32013R1024).
//  - Uredba number was constrained to 4 digits, missing 3-digit references like
//    "596/2014". Loosened to \d+.

const PATTERN =
  /(Direktiva\s+(\d{4})\/(\d+)\/(?:ES|EU|EGS|Euratom))|(Odločba\s+(\d{4})\/(\d+)\/(?:ES|EU|EGS))|(Sklep\s+(\d{4})\/(\d+)\/(?:EU|ES|EGS))|(Uredba\s+\((?:EU|ES|EGS|Euratom)\)\s+(?:št\.\s+)?(\d+)\/(\d{4}))/g;

export function remarkEuLinks() {
  return (tree: Root) => {
    visit(tree, 'text', (node: Text, indexInParent, parent: Parent | undefined) => {
      if (!parent || indexInParent == null) return;
      if (parent.type === 'link' || parent.type === 'linkReference') return;
      if (parent.type === 'code' || parent.type === 'inlineCode') return;

      const text = node.value;
      if (!PATTERN.test(text)) return;
      PATTERN.lastIndex = 0;

      const children: Node[] = [];
      let last = 0;
      let m: RegExpExecArray | null;
      while ((m = PATTERN.exec(text)) !== null) {
        let year: string;
        let num: string;
        let typeChar: 'L' | 'D' | 'R';
        if (m[1]) {
          year = m[2];
          num = m[3];
          typeChar = 'L';
        } else if (m[4]) {
          year = m[5];
          num = m[6];
          typeChar = 'D';
        } else if (m[7]) {
          year = m[8];
          num = m[9];
          typeChar = 'D';
        } else {
          // Uredba is NNN/YYYY (number first, year second) — opposite of the others.
          num = m[11];
          year = m[12];
          typeChar = 'R';
        }
        const celex = `3${year}${typeChar}${num.padStart(4, '0')}`;
        const url = `https://eur-lex.europa.eu/legal-content/SL/TXT/?uri=CELEX:${celex}`;
        const matchText = m[0];

        if (m.index > last) children.push({ type: 'text', value: text.slice(last, m.index) } as Text);
        children.push({
          type: 'link',
          url,
          title: `EUR-Lex ${celex}`,
          data: { hProperties: { className: ['eu-ref'], target: '_blank', rel: 'noopener' } },
          children: [{ type: 'text', value: matchText } as Text],
        } as unknown as Node);
        last = m.index + matchText.length;
      }
      if (children.length === 0) return;
      if (last < text.length) children.push({ type: 'text', value: text.slice(last) } as Text);

      parent.children.splice(indexInParent, 1, ...(children as Parent['children']));
      return [SKIP, indexInParent + children.length];
    });
  };
}
