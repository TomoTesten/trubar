'use client';

// Client island: print only fires from the browser. The rest of the sidebar
// stays as RSC so we don't ship JS for static metadata.

export function PrintButton({ className }: { className?: string }) {
  return (
    <button type="button" onClick={() => window.print()} className={className}>
      🖨 Natisni / PDF
    </button>
  );
}
