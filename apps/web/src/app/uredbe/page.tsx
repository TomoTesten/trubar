import { CategoryPage } from '@/components/CategoryPage';

export const metadata = { title: 'Uredbe' };
export const revalidate = 3600;

export default function Page() {
  return (
    <CategoryPage
      title="Uredbe"
      description="Uredbe Vlade Republike Slovenije."
      vrsta="uredba"
    />
  );
}
