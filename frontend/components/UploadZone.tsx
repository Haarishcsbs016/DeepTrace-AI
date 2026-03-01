'use client';

import { useCallback, useState } from 'react';
import { Upload, Image, Video, Mic } from 'lucide-react';
import clsx from 'clsx';

type MediaType = 'image' | 'video' | 'audio';

const ACCEPT: Record<MediaType, string> = {
  image: 'image/jpeg,image/png,image/webp',
  video: 'video/mp4,video/webm,video/avi',
  audio: 'audio/wav,audio/mpeg,audio/mp3,audio/webm',
};

interface UploadZoneProps {
  mediaType: MediaType;
  onFile: (file: File) => void;
  disabled?: boolean;
}

const labels: Record<MediaType, { title: string; icon: React.ReactNode }> = {
  image: { title: 'Image', icon: <Image className="w-8 h-8" /> },
  video: { title: 'Video', icon: <Video className="w-8 h-8" /> },
  audio: { title: 'Audio', icon: <Mic className="w-8 h-8" /> },
};

export function UploadZone({ mediaType, onFile, disabled }: UploadZoneProps) {
  const [drag, setDrag] = useState(false);
  const { title, icon } = labels[mediaType];

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault();
      setDrag(false);
      if (disabled) return;
      const file = e.dataTransfer.files[0];
      if (file) onFile(file);
    },
    [onFile, disabled]
  );

  const handleChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const file = e.target.files?.[0];
      if (file) onFile(file);
      e.target.value = '';
    },
    [onFile]
  );

  return (
    <label
      className={clsx(
        'relative flex flex-col items-center justify-center rounded-xl border-2 border-dashed p-10 transition-all cursor-pointer',
        'bg-dark-800 border-dark-600 hover:border-accent-blue/50 hover:bg-dark-700',
        drag && 'border-accent-purple bg-dark-700',
        disabled && 'opacity-60 cursor-not-allowed'
      )}
      onDragOver={(e) => {
        e.preventDefault();
        setDrag(true);
      }}
      onDragLeave={() => setDrag(false)}
      onDrop={handleDrop}
    >
      <div className="absolute inset-0 overflow-hidden rounded-xl">
        <div className="scan-line absolute left-0 right-0 top-1/2 -translate-y-1/2 w-full" />
      </div>
      <span className="text-accent-blue mb-2">{icon}</span>
      <span className="text-lg font-medium text-slate-200">{title} Deepfake Detection</span>
      <span className="text-sm text-slate-400 mt-1">Drag & drop or click to upload</span>
      <input
        type="file"
        accept={ACCEPT[mediaType]}
        onChange={handleChange}
        disabled={disabled}
        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer disabled:cursor-not-allowed"
      />
    </label>
  );
}
