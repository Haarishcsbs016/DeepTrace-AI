'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { UploadZone } from '@/components/UploadZone';
import { ResultPanel } from '@/components/ResultPanel';
import { HistoryTable } from '@/components/HistoryTable';
import { getHistory, detectImage, detectVideo, detectAudio, me, logout } from '@/lib/api';
import type { HistoryItem } from '@/components/HistoryTable';
import type { DetectionResultData } from '@/components/ResultPanel';
import { Shield, LogOut } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();
  const [user, setUser] = useState<{ email: string } | null>(null);
  const [tab, setTab] = useState<'image' | 'video' | 'audio'>('image');
  const [result, setResult] = useState<DetectionResultData | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);

  useEffect(() => {
    me().then((u) => {
      if (!u) router.replace('/');
      else setUser(u);
    });
  }, [router]);

  useEffect(() => {
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    if (!token) return;
    getHistory().then((r) => setHistory(r.items || []));
  }, [result]);

  const handleFile = async (file: File) => {
    setError(null);
    setResult(null);
    setLoading(true);
    try {
      let data: { result: DetectionResultData };
      if (tab === 'image') data = await detectImage(file);
      else if (tab === 'video') data = await detectVideo(file);
      else data = await detectAudio(file);
      setResult(data.result);
      setHistory((prev) => [
        {
          id: data.result.report_id || '',
          report_id: data.result.report_id || '',
          media_type: tab,
          label: data.result.label,
          confidence: data.result.confidence,
        },
        ...prev,
      ]);
    } catch (e) {
      setError(e instanceof Error ? e.message : 'Detection failed');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    logout();
    router.replace('/');
  };

  if (!user) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="w-10 h-10 border-2 border-accent-blue border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-dark-900">
      <header className="border-b border-dark-600 bg-dark-800/80 backdrop-blur">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Shield className="w-8 h-8 text-accent-blue" />
            <span className="font-semibold text-lg">Deepfake Detection</span>
          </div>
          <div className="flex items-center gap-4">
            <span className="text-slate-400 text-sm">{user.email}</span>
            <button
              type="button"
              onClick={handleLogout}
              className="flex items-center gap-2 px-3 py-1.5 rounded-lg text-slate-400 hover:bg-dark-600 hover:text-slate-200"
            >
              <LogOut className="w-4 h-4" /> Logout
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-4">
          {(['image', 'video', 'audio'] as const).map((t) => (
            <button
              key={t}
              type="button"
              onClick={() => setTab(t)}
              className={`py-2 px-4 rounded-lg font-medium capitalize transition ${
                tab === t
                  ? 'bg-gradient-to-r from-accent-blue/20 to-accent-purple/20 text-accent-blue border border-accent-blue/40'
                  : 'bg-dark-800 text-slate-400 hover:text-slate-200 border border-dark-600'
              }`}
            >
              {t}
            </button>
          ))}
        </div>

        <section className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-10">
          <div>
            <h3 className="text-slate-300 font-medium mb-3">Upload {tab}</h3>
            <UploadZone mediaType={tab} onFile={handleFile} disabled={loading} />
          </div>
          <div>
            <h3 className="text-slate-300 font-medium mb-3">Result</h3>
            <ResultPanel result={result} loading={loading} error={error} mediaType={tab} />
          </div>
        </section>

        <section>
          <h3 className="text-slate-300 font-medium mb-3">History</h3>
          <HistoryTable items={history} onRefresh={() => getHistory().then((r) => setHistory(r.items || []))} />
        </section>
      </main>
    </div>
  );
}
