const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

function getToken(): string | null {
  if (typeof window === 'undefined') return null;
  return localStorage.getItem('token');
}

export async function register(email: string, password: string, fullName?: string) {
  const res = await fetch(`${API_BASE}/auth/register`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password, full_name: fullName || null }),
  });
  if (!res.ok) {
    const d = await res.json().catch(() => ({}));
    throw new Error(d.detail || 'Registration failed');
  }
  return res.json();
}

export async function login(email: string, password: string) {
  const res = await fetch(`${API_BASE}/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    const d = await res.json().catch(() => ({}));
    throw new Error(d.detail || 'Login failed');
  }
  const data = await res.json();
  if (typeof window !== 'undefined' && data.access_token) {
    localStorage.setItem('token', data.access_token);
  }
  return data;
}

export function logout() {
  if (typeof window !== 'undefined') localStorage.removeItem('token');
}

export async function me() {
  const token = getToken();
  if (!token) return null;
  const res = await fetch(`${API_BASE}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return null;
  return res.json();
}

export async function detectImage(file: File) {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_BASE}/detect/image`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (!res.ok) {
    const d = await res.json().catch(() => ({}));
    throw new Error(d.detail || 'Detection failed');
  }
  return res.json();
}

export async function detectVideo(file: File) {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_BASE}/detect/video`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (!res.ok) {
    const d = await res.json().catch(() => ({}));
    throw new Error(d.detail || 'Detection failed');
  }
  return res.json();
}

export async function detectAudio(file: File) {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const form = new FormData();
  form.append('file', file);
  const res = await fetch(`${API_BASE}/detect/audio`, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: form,
  });
  if (!res.ok) {
    const d = await res.json().catch(() => ({}));
    throw new Error(d.detail || 'Detection failed');
  }
  return res.json();
}

export async function getHistory() {
  const token = getToken();
  if (!token) return { items: [] };
  const res = await fetch(`${API_BASE}/results/history`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) return { items: [] };
  return res.json();
}

export async function downloadReport(reportId: string) {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  const res = await fetch(`${API_BASE}/results/report/${reportId}/download`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  if (!res.ok) throw new Error('Download failed');
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `deepfake_report_${reportId}.json`;
  a.click();
  URL.revokeObjectURL(url);
}
