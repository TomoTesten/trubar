// Port of build_site.py:125-131 `status_badge`. Classifies free-text status
// strings into one of three buckets so the UI can render a colored tag.

type Status = 'valid' | 'invalid' | 'neutral';

function classify(status: string | undefined): { kind: Status; label: string } {
  const s = (status ?? '').toLowerCase();
  if (s.includes('nevel') || s.includes('pretekl')) return { kind: 'invalid', label: 'neveljaven' };
  if (s.includes('vel')) return { kind: 'valid', label: 'veljaven' };
  return { kind: 'neutral', label: status ?? '' };
}

const classes: Record<Status, string> = {
  valid: 'bg-emerald-100 text-emerald-900 dark:bg-emerald-900/40 dark:text-emerald-200',
  invalid: 'bg-rose-100 text-rose-900 dark:bg-rose-900/40 dark:text-rose-200',
  neutral: 'bg-muted text-muted-foreground',
};

export function StatusBadge({ status }: { status: string | undefined }) {
  const { kind, label } = classify(status);
  if (!label) return null;
  return (
    <span
      className={`inline-flex items-center rounded-md px-2 py-0.5 text-xs font-medium ${classes[kind]}`}
    >
      {label}
    </span>
  );
}
