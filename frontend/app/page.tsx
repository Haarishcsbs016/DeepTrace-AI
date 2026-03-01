'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { AuthForm } from '@/components/AuthForm';
import { me } from '@/lib/api';
import { Shield } from 'lucide-react';

export default function HomePage() {
  const router = useRouter();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    me().then((user) => {
      setChecking(false);
      if (user) router.replace('/dashboard');
    });
  }, [router]);

  if (checking) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-dark-900">
        <div className="w-10 h-10 border-2 border-accent-blue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-dark-900 bg-gradient-subtle p-4">
      <div className="flex items-center gap-2 mb-8">
        <Shield className="w-10 h-10 text-accent-blue" />
        <h1 className="text-2xl font-bold text-slate-100">AI Deepfake Detection</h1>
      </div>
      <p className="text-slate-400 text-center max-w-md mb-8">
        Analyze images, video, and audio for synthetic manipulation. Get confidence scores and forensic reports.
      </p>
      <AuthForm onSuccess={() => router.replace('/dashboard')} />
    </div>
  );
}
