import './globals.css';

export const metadata = {
  title: 'Sentiment Lab | آزمایشگاه تحلیل احساسات امیرحسین رضایی',
  description: 'روایت تعاملی تحلیل احساسات؛ از استخراج دیدگاه تا پیش‌بینی، ساخته‌شده توسط امیرحسین رضایی.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="fa" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
