import { CategoryPage } from '@/components/CategoryPage';

export const metadata = { title: 'Lokalni predpisi' };
export const revalidate = 3600;

export default function Page() {
  return (
    <CategoryPage
      title="Lokalni predpisi"
      description="Občinski odloki, sklepi in pravilniki. Rows odpirajo izvirno objavo na Uradnem listu RS."
      vrsta={['občinski odlok', 'občinski sklep', 'občinski pravilnik']}
      externalLink
    />
  );
}
