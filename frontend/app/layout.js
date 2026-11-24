import './globals.css';

export const metadata = {
  title: 'از یک نظر تا یک تصمیم | آزمایشگاه تحلیل احساسات',
  description: 'روایت تعاملی مسیر تحلیل احساسات؛ از استخراج دیدگاه تا پیش‌بینی مثبت یا منفی بودن آن.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="fa" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
