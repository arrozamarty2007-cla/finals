import { useState } from 'react';
import { ArrowUpRight, X } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function PopupLogin({ isLoginVisible, setLoginVisible }) {
  const [isRegister, setIsRegister] = useState(false);
  const [form, setForm] = useState({ username: '', email: '', password: '', confirm_password: '', first_name: '', last_name: '' });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { signIn } = useAuth();

  if (!isLoginVisible) return null;

  function update(field, value) {
    setForm(current => ({ ...current, [field]: value }));
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setError('');
    setLoading(true);
    try {
      const payload = isRegister ? form : { username: form.username, password: form.password };
      await signIn(payload, isRegister);
      setLoginVisible(false);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="modal-backdrop" onMouseDown={event => event.target === event.currentTarget && setLoginVisible(false)}>
      <section className="login-modal">
        <button className="modal-x" onClick={() => setLoginVisible(false)} aria-label="Close"><X size={19} /></button>
        <p className="eyebrow">WELCOME TO THREADLINE</p>
        <h2>{isRegister ? 'Create your account.' : 'Good to see you.'}</h2>
        <p className="muted-copy">Sign in to keep your favorite pieces close.</p>
        <form onSubmit={handleSubmit} className="login-form">
          {isRegister && <>
            <input placeholder="First name" value={form.first_name} onChange={e => update('first_name', e.target.value)} />
            <input placeholder="Last name" value={form.last_name} onChange={e => update('last_name', e.target.value)} />
            <input type="email" placeholder="Email address" required value={form.email} onChange={e => update('email', e.target.value)} />
          </>}
          <input placeholder="Username" required value={form.username} onChange={e => update('username', e.target.value)} />
          <input type="password" placeholder="Password" required value={form.password} onChange={e => update('password', e.target.value)} />
          {isRegister && <input type="password" placeholder="Confirm password" required value={form.confirm_password} onChange={e => update('confirm_password', e.target.value)} />}
          {error && <p className="form-error">{error}</p>}
          <button className="dark-button full-button" disabled={loading}>{loading ? 'Please wait…' : isRegister ? 'Create account' : 'Sign in'} <ArrowUpRight size={16} /></button>
        </form>
        <p className="switch-line">{isRegister ? 'Already have an account?' : 'New to THREADLINE?'} <button onClick={() => { setIsRegister(!isRegister); setError(''); }}> {isRegister ? 'Sign in' : 'Create an account'}</button></p>
      </section>
    </section>
  );
}
