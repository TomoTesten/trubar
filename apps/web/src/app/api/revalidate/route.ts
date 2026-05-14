import { NextResponse } from 'next/server';
import { revalidatePath } from 'next/cache';

// POST /api/revalidate
// Headers: Authorization: Bearer ${REVALIDATE_TOKEN}
// Body:    { "paths": ["/ZKP", "/npb/ANJP299"] }
//
// Called by .github/workflows/revalidate.yml on each push to master, with the
// paths derived from `git diff` of changed si/**.md files. Each path is
// passed to Next.js's revalidatePath, busting the ISR cache so the next
// request renders fresh content.

const MAX_PATHS = 200; // a single commit shouldn't touch this many laws

export async function POST(request: Request) {
  const token = process.env.REVALIDATE_TOKEN;
  if (!token) {
    return NextResponse.json({ error: 'REVALIDATE_TOKEN not configured' }, { status: 500 });
  }
  const auth = request.headers.get('authorization');
  if (auth !== `Bearer ${token}`) {
    return NextResponse.json({ error: 'unauthorized' }, { status: 401 });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return NextResponse.json({ error: 'invalid json' }, { status: 400 });
  }

  const paths = (body as { paths?: unknown })?.paths;
  if (!Array.isArray(paths) || paths.length === 0) {
    return NextResponse.json({ error: 'paths array required' }, { status: 400 });
  }
  if (paths.length > MAX_PATHS) {
    return NextResponse.json({ error: `too many paths (max ${MAX_PATHS})` }, { status: 400 });
  }

  const revalidated: string[] = [];
  for (const p of paths) {
    if (typeof p !== 'string' || !p.startsWith('/')) continue;
    revalidatePath(p);
    revalidated.push(p);
  }

  return NextResponse.json({ revalidated, count: revalidated.length });
}
