import { createContext, useContext, useEffect, useState } from 'react';
import { apiRequest } from '../api/config';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('threadline_token') || '');

  useEffect(() => {
    if (!token) return;
    apiRequest('/auth/me/').then(setUser).catch(() => {
      localStorage.removeItem('threadline_token');
      setToken('');
      setUser(null);
    });
  }, [token]);

  async function signIn(credentials, isRegister = false) {
    const path = isRegister ? '/auth/register/' : '/auth/login/';
    const result = await apiRequest(path, {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    localStorage.setItem('threadline_token', result.token);
    setToken(result.token);
    setUser(result.user);
    return result.user;
  }

  async function signOut() {
    try { await apiRequest('/auth/logout/', { method: 'POST' }); } catch { /* local sign out still works */ }
    localStorage.removeItem('threadline_token');
    setToken('');
    setUser(null);
  }

  return <AuthContext.Provider value={{ user, token, signIn, signOut }}>
    {children}
  </AuthContext.Provider>;
}

export function useAuth() {
  return useContext(AuthContext);
}
