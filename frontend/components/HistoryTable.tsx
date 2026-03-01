'use client';

import { Download } from 'lucide-react';
import { downloadReport } from '@/lib/api';

export interface HistoryItem {
  id: string;
  report_id: string;
  media_type: string;
  label: string;
  confidence: number;
  created_at?: string;
}

interface HistoryTableProps {
  items: HistoryItem[];
  onRefresh: () => void;
}

export function HistoryTable({ items, onRefresh }: HistoryTableProps) {
  const handleDownload = (reportId: string) => {
    downloadReport(reportId).catch(console.error);
  };

  if (items.length === 0) {
    return (
      <div className="rounded-xl bg-dark-800 border border-dark-600 p-8 text-center text-slate-500">
        <p>No detection history yet. Run an analysis to see results here.</p>
      </div>
    );
  }

  return (
    <div className="rounded-xl bg-dark-800 border border-dark-600 overflow-hidden">
      <table className="w-full text-left">
        <thead>
          <tr className="border-b border-dark-600 bg-dark-700/50">
            <th className="px-4 py-3 text-slate-400 font-medium">Report ID</th>
            <th className="px-4 py-3 text-slate-400 font-medium">Type</th>
            <th className="px-4 py-3 text-slate-400 font-medium">Verdict</th>
            <th className="px-4 py-3 text-slate-400 font-medium">Confidence</th>
            <th className="px-4 py-3 text-slate-400 font-medium w-24">Report</th>
          </tr>
        </thead>
        <tbody>
          {items.map((row) => (
            <tr key={row.id} className="border-b border-dark-600/50 hover:bg-dark-700/30">
              <td className="px-4 py-3 text-slate-300 font-mono text-sm">{row.report_id?.slice(0, 8)}...</td>
              <td className="px-4 py-3 text-slate-300 capitalize">{row.media_type}</td>
              <td className="px-4 py-3">
                <span className={row.label === 'fake' ? 'text-red-400' : 'text-green-400'}>{row.label}</span>
              </td>
              <td className="px-4 py-3 text-slate-300">{(row.confidence * 100).toFixed(1)}%</td>
              <td className="px-4 py-3">
                <button
                  type="button"
                  onClick={() => handleDownload(row.report_id)}
                  className="p-2 rounded-lg hover:bg-dark-600 text-slate-400 hover:text-accent-blue"
                  title="Download forensic report"
                >
                  <Download className="w-4 h-4" />
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
