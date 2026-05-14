import { CategoryPage } from '@/components/CategoryPage';

export const metadata = { title: 'Pravilniki' };
export const revalidate = 3600;

export default function Page() {
  return (
    <CategoryPage
      title="Pravilniki"
      description="Pravilniki ministrstev in drugih organov."
      vrsta="pravilnik"
    />
  );
}
