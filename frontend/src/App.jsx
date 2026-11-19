import { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import { ArrowUpRight, Menu, ShoppingBag, UserRound, X } from 'lucide-react';
import PopupLogin from './components/popups/PopupLogin';
import { useAuth } from './context/AuthContext';

export default function App() {
  const [isLoginVisible, setLoginVisible] = useState(false);
  const [menuOpen, setMenuOpen] = useState(false);
  const { user, signOut } = useAuth();
  const navigate = useNavigate();

  async function handleSignOut() {
    await signOut();
    navigate('/shop');
  }

  return (
    <main className="site-shell">
      <div className="topline">COMPLIMENTARY SHIPPING ON ORDERS OVER ₱2,500</div>
      {isLoginVisible && <PopupLogin isLoginVisible={isLoginVisible} setLoginVisible={setLoginVisible} />}

      <header className="site-header">
        <button className="mobile-menu icon-button" onClick={() => setMenuOpen(!menuOpen)} aria-label="Toggle menu">
          {menuOpen ? <X size={20} /> : <Menu size={20} />}
        </button>
        <NavLink to="/shop" className="brand">THREADLINE<span>®</span></NavLink>
        <nav className={`main-nav ${menuOpen ? 'nav-open' : ''}`}>
          <NavLink to="/shop" onClick={() => setMenuOpen(false)}>Shop</NavLink>
          <a href="/shop#collection" onClick={() => setMenuOpen(false)}>Collection</a>
          <NavLink to="/orders" onClick={() => setMenuOpen(false)}>My orders</NavLink>
        </nav>
        <div className="header-actions">
          {user ? (
            <>
              <span className="hello-user"><UserRound size={16} /> {user.first_name || user.username}</span>
              <button className="text-action" onClick={handleSignOut}>Sign out</button>
            </>
          ) : (
            <button className="text-action account-action" onClick={() => setLoginVisible(true)}><UserRound size={16} /> Account</button>
          )}
          <NavLink to="/cart" className="bag-link"><ShoppingBag size={17} /> Bag <ArrowUpRight size={13} /></NavLink>
        </div>
      </header>

      <Outlet context={{ openLogin: () => setLoginVisible(true) }} />

      <footer className="site-footer">
        <div><NavLink to="/shop" className="brand">THREADLINE<span>®</span></NavLink><p>Considered clothing for everyday living.</p></div>
        <span>© 2026 THREADLINE. MADE FOR EVERY DAY.</span>
      </footer>
    </main>
  );
}
