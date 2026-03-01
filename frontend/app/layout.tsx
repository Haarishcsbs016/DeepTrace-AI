import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'Deepfake Detection | AI-Powered Verification',
  description: 'Detect deepfakes in images, video, and audio with AI.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-dark-900 text-slate-100">
        {children}
      </body>
    </html>
  );
}
