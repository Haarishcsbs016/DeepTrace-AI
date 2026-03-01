'use client';

import { ConfidenceMeter } from './ConfidenceMeter';

export interface DetectionResultData {
  label: 'real' | 'fake';
  confidence: number;
  confidence_real?: number;
  confidence_fake?: number;
  report_id?: string;
  frame_scores?: number[];
  timeline?: { frame: number; score: number; anomaly: boolean }[];
}

interface ResultPanelProps {
  result: DetectionResultData | null;
  loading?: boolean;
  error?: string | null;
  mediaType?: 'image' | 'video' | 'audio';
}

export function ResultPanel({ result, loading, error, mediaType }: ResultPanelProps) {
  if (loading) {
    return (
      <div className="rounded-xl bg-dark-800 border border-dark-600 p-8 flex flex-col items-center justify-center min-h-[240px]">
        <div className="w-12 h-12 border-2 border-accent-blue border-t-transparent rounded-full animate-spin" />
        <p className="mt-4 text-slate-400">Analyzing with AI...</p>
        <p className="text-sm text-slate-500">Face extraction & artifact detection</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl bg-dark-800 border border-red-500/30 p-8 text-center">
        <p className="text-red-400">{error}</p>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="rounded-xl bg-dark-800 border border-dark-600 p-8 flex flex-col items-center justify-center min-h-[240px] text-slate-500">
        <p>Result will appear here after analysis</p>
      </div>
    );
  }

  const confidence = result.confidence ?? (result.label === 'real' ? (result.confidence_real ?? 0.5) : (result.confidence_fake ?? 0.5));

  return (
    <div className="rounded-xl bg-dark-800 border border-dark-600 p-8">
      <div className="flex flex-wrap gap-8 items-center justify-center">
        <ConfidenceMeter confidence={confidence} label={result.label} />
        <div className="flex-1 min-w-[200px] space-y-2">
          <p className="text-slate-400">
            Verdict: <span className={result.label === 'fake' ? 'text-red-400' : 'text-green-400'}>{result.label}</span>
          </p>
          {result.confidence_real != null && (
            <p className="text-sm text-slate-500">Real: {(result.confidence_real * 100).toFixed(1)}%</p>
          )}
          {result.confidence_fake != null && (
            <p className="text-sm text-slate-500">Fake: {(result.confidence_fake * 100).toFixed(1)}%</p>
          )}
          {result.report_id && (
            <p className="text-xs text-slate-600 mt-2">Report ID: {result.report_id.slice(0, 8)}...</p>
          )}
        </div>
      </div>
      {mediaType === 'video' && result.timeline && result.timeline.length > 0 && (
        <div className="mt-6 pt-6 border-t border-dark-600">
          <p className="text-sm text-slate-400 mb-2">Frame anomaly timeline</p>
          <div className="flex gap-1 flex-wrap">
            {result.timeline.slice(0, 40).map((t, i) => (
              <div
                key={i}
                className="w-2 h-6 rounded-sm"
                style={{
                  backgroundColor: t.anomaly ? 'rgba(239,68,68,0.8)' : 'rgba(34,197,94,0.4)',
                }}
                title={`Frame ${t.frame}: ${(t.score * 100).toFixed(0)}%`}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
