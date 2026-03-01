'use client';

interface ConfidenceMeterProps {
  confidence: number; // 0-1
  label: 'real' | 'fake';
  size?: number;
}

export function ConfidenceMeter({ confidence, label, size = 140 }: ConfidenceMeterProps) {
  const percent = Math.round(confidence * 100);
  const circumference = 2 * Math.PI * 45;
  const offset = circumference - (percent / 100) * circumference;
  const isFake = label === 'fake';

  return (
    <div className="flex flex-col items-center">
      <svg width={size} height={size} className="transform -rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r="45"
          fill="none"
          stroke="currentColor"
          strokeWidth="8"
          className="text-dark-600"
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r="45"
          fill="none"
          strokeWidth="8"
          strokeLinecap="round"
          className="circle-progress transition-all duration-700"
          style={{
            stroke: isFake ? '#ef4444' : '#22c55e',
            strokeDasharray: circumference,
            strokeDashoffset: offset,
          }}
        />
      </svg>
      <span className="text-3xl font-bold mt-2 text-slate-100">{percent}%</span>
      <span className={isFake ? 'text-red-400' : 'text-green-400'}>{label.toUpperCase()}</span>
    </div>
  );
}
