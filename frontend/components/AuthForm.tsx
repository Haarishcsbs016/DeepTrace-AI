'use client';

import { useState } from 'react';
import { login, register } from '@/lib/api';
import clsx from 'clsx';

interface AuthFormProps {
  onSuccess: () => void;
}

export function AuthForm({ onSuccess }: AuthFormProps) {
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [fullName, setFullName] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setLoading(true);
    try {
      if (mode === 'login') {
        await login(email, password);
      } else {
        await register(email, password, fullName || undefined);
        await login(email, password);
      }
      onSuccess();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Something went wrong');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto rounded-2xl bg-dark-800 border border-dark-600 p-8 shadow-xl">
      <h2 className="text-2xl font-bold bg-gradient-to-r from-accent-blue to-accent-purple bg-clip-text text-transparent">
        Deepfake Detection
      </h2>
      <p className="text-slate-400 mt-1 mb-6">Sign in to analyze media</p>

      <form onSubmit={submit} className="space-y-4">
        <div>
          <label className="block text-sm text-slate-400 mb-1">Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-lg bg-dark-700 border border-dark-600 text-slate-100 placeholder-slate-500 focus:border-accent-blue focus:ring-1 focus:ring-accent-blue outline-none"
            placeholder="you@example.com"
          />
        </div>
        {mode === 'register' && (
          <div>
            <label className="block text-sm text-slate-400 mb-1">Full name</label>
            <input
              type="text"
              value={fullName}
              onChange={(e) => setFullName(e.target.value)}
              className="w-full px-4 py-2 rounded-lg bg-dark-700 border border-dark-600 text-slate-100 placeholder-slate-500 focus:border-accent-blue outline-none"
              placeholder="Optional"
            />
          </div>
        )}
        <div>
          <label className="block text-sm text-slate-400 mb-1">Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="w-full px-4 py-2 rounded-lg bg-dark-700 border border-dark-600 text-slate-100 placeholder-slate-500 focus:border-accent-blue outline-none"
            placeholder="••••••••"
          />
        </div>
        {error && <p className="text-red-400 text-sm">{error}</p>}
        <button
          type="submit"
          disabled={loading}
          className={clsx(
            'w-full py-2.5 rounded-lg font-medium bg-gradient-to-r from-accent-blue to-accent-purple text-white',
            'hover:opacity-90 transition disabled:opacity-60'
          )}
        >
          {loading ? 'Please wait...' : mode === 'login' ? 'Sign in' : 'Create account'}
        </button>
      </form>

      <button
        type="button"
        onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
        className="mt-4 text-sm text-slate-400 hover:text-accent-blue"
      >
        {mode === 'login' ? "Don't have an account? Register" : 'Already have an account? Sign in'}
      </button>
    </div>
  );
}
