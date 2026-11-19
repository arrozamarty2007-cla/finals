export const API_URL = 'http://127.0.0.1:8000/api';

export function getHeaders(token = localStorage.getItem('threadline_token')) {
  return {
    'Content-Type': 'application/json',
    ...(token ? { Authorization: `Token ${token}` } : {}),
  };
}

export async function apiRequest(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: { ...getHeaders(), ...(options.headers || {}) },
  });
  if (response.status === 204) return null;
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = data.detail || Object.values(data).flat().join(' ') || 'Something went wrong.';
    throw new Error(message);
  }
  return data;
}
