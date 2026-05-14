import { ImageResponse } from 'next/og';

export const alt = 'T.R.U.B.A.R. — slovenska zakonodaja';
export const size = { width: 1200, height: 630 };
export const contentType = 'image/png';

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'space-between',
          padding: 64,
          background: 'linear-gradient(135deg, #fafafa 0%, #f0f0f0 100%)',
          fontFamily: 'sans-serif',
        }}
      >
        <div
          style={{
            fontSize: 28,
            letterSpacing: 8,
            color: '#666',
            textTransform: 'uppercase',
          }}
        >
          T.R.U.B.A.R.
        </div>
        <div
          style={{
            fontSize: 72,
            lineHeight: 1.05,
            fontWeight: 700,
            color: '#111',
            letterSpacing: -1,
          }}
        >
          Slovenska zakonodaja kot Git repozitorij
        </div>
        <div style={{ fontSize: 26, color: '#666' }}>
          Zakoni, uredbe, pravilniki in prečiščena besedila. 1946 → danes.
        </div>
      </div>
    ),
    { ...size },
  );
}
