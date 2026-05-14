import { CategoryPage } from '@/components/CategoryPage';

export const metadata = { title: 'Zakoni' };
export const revalidate = 3600;

export default function Page() {
  return (
    <CategoryPage
      title="Zakoni"
      description="Sprejeti zakoni Državnega zbora Republike Slovenije."
      vrsta="Sprejet zakon"
    />
  );
}
