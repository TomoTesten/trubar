'use client';

// Client island wrapping react-diff-viewer-continued. The library uses CSS-in-JS
// and depends on browser-only APIs (window.matchMedia for the mobile mode
// toggle), so it lives behind a 'use client' boundary.

import { useEffect, useState } from 'react';
import ReactDiffViewer, { DiffMethod } from 'react-diff-viewer-continued';

type Props = {
  oldValue: string;
  newValue: string;
  leftTitle: string;
  rightTitle: string;
};

export function DiffViewer({ oldValue, newValue, leftTitle, rightTitle }: Props) {
  // Side-by-side on wide screens; unified (split=false) on mobile.
  const [splitView, setSplitView] = useState(true);
  useEffect(() => {
    const mq = window.matchMedia('(max-width: 700px)');
    const apply = () => setSplitView(!mq.matches);
    apply();
    mq.addEventListener('change', apply);
    return () => mq.removeEventListener('change', apply);
  }, []);

  return (
    <div className="overflow-x-auto rounded-md border border-border bg-card text-xs">
      <ReactDiffViewer
        oldValue={oldValue}
        newValue={newValue}
        leftTitle={leftTitle}
        rightTitle={rightTitle}
        splitView={splitView}
        compareMethod={DiffMethod.WORDS}
        useDarkTheme={false}
      />
    </div>
  );
}
