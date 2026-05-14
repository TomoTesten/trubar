import type { NextConfig } from 'next';

// 308 permanent redirects from the old GitHub Pages URL shape (/trubar/...)
// to the new app's URL shape. Active once DNS is pointed at this app — until
// then they're harmless no-ops on the Vercel subdomain.
const nextConfig: NextConfig = {
  async redirects() {
    return [
      // Law detail pages: /trubar/si/ZKP/  →  /ZKP
      { source: '/trubar/si/:kratica/', destination: '/:kratica', permanent: true },
      { source: '/trubar/si/:kratica', destination: '/:kratica', permanent: true },

      // NPB pages
      { source: '/trubar/npb/:kratica/', destination: '/npb/:kratica', permanent: true },
      { source: '/trubar/npb/:kratica', destination: '/npb/:kratica', permanent: true },

      // Category listings (with and without trailing slash)
      { source: '/trubar/zakoni/', destination: '/zakoni', permanent: true },
      { source: '/trubar/zakoni', destination: '/zakoni', permanent: true },
      { source: '/trubar/uredbe/', destination: '/uredbe', permanent: true },
      { source: '/trubar/uredbe', destination: '/uredbe', permanent: true },
      { source: '/trubar/pravilniki/', destination: '/pravilniki', permanent: true },
      { source: '/trubar/pravilniki', destination: '/pravilniki', permanent: true },
      { source: '/trubar/npb/', destination: '/npb', permanent: true },
      { source: '/trubar/lokalni/', destination: '/lokalni', permanent: true },
      { source: '/trubar/lokalni', destination: '/lokalni', permanent: true },

      // Compare tool (preserves ?a=…&b=…)
      { source: '/trubar/primerjaj/', destination: '/primerjaj', permanent: true },
      { source: '/trubar/primerjaj', destination: '/primerjaj', permanent: true },

      // DuckDB-WASM page is dropped — redirect to home (mentioned in CHANGELOG).
      { source: '/trubar/sql/', destination: '/', permanent: true },
      { source: '/trubar/sql', destination: '/', permanent: true },

      // Old root.
      { source: '/trubar/', destination: '/', permanent: true },
      { source: '/trubar', destination: '/', permanent: true },
    ];
  },
};

export default nextConfig;
