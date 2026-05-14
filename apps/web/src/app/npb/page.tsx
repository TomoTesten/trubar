import { CategoryPage } from '@/components/CategoryPage';

export const metadata = { title: 'Neuradna prečiščena besedila (NPB)' };
export const revalidate = 3600;

export default function Page() {
  return (
    <CategoryPage
      title="Neuradna prečiščena besedila"
      description="Konsolidirana besedila predpisov iz PISRS. Združujejo izvirno besedilo s kasnejšimi spremembami."
      vrsta="NPB"
      urlPrefix="/npb/"
    />
  );
}
