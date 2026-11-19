import { useEffect, useState } from 'react';
import { Link, useNavigate, useOutletContext } from 'react-router-dom';
import { Minus, Plus, Trash2 } from 'lucide-react';
import { apiRequest } from '../api/config';
import { useAuth } from '../context/AuthContext';

const peso = value => `₱${Number(value || 0).toLocaleString('en-PH', { minimumFractionDigits: 2 })}`;

export default function Cart() {
  const [items, setItems] = useState([]);
  const [message, setMessage] = useState('');
  const [busy, setBusy] = useState(false);
  const { user } = useAuth();
  const { openLogin } = useOutletContext();
  const navigate = useNavigate();

  async function loadCart() {
    try { setItems(await apiRequest('/cart/')); } catch (error) { setMessage(error.message); }
  }
  useEffect(() => { if (user) loadCart(); else setItems([]); }, [user]);

  async function updateQuantity(item, quantity) {
    if (quantity < 1) return;
    try {
      const updated = await apiRequest(`/cart/items/${item.id}/`, { method: 'PATCH', body: JSON.stringify({ quantity }) });
      setItems(current => current.map(line => line.id === item.id ? updated : line));
    } catch (error) { setMessage(error.message); }
  }

  async function removeItem(id) {
    try { await apiRequest(`/cart/items/${id}/`, { method: 'DELETE' }); setItems(current => current.filter(item => item.id !== id)); }
    catch (error) { setMessage(error.message); }
  }

  async function checkout() {
    setBusy(true);
    try { await apiRequest('/checkout/', { method: 'POST' }); navigate('/orders', { state: { justOrdered: true } }); }
    catch (error) { setMessage(error.message); }
    finally { setBusy(false); }
  }

  const total = items.reduce((sum, item) => sum + Number(item.product_detail.price) * item.quantity, 0);
  if (!user) return <section className="empty-state"><p className="eyebrow">YOUR SELECTION</p><h1>Your bag is waiting.</h1><p>Sign in to see the pieces you've saved.</p><button className="dark-button" onClick={openLogin}>Sign in to continue</button></section>;

  return <section className="inner-page"><p className="eyebrow">YOUR SELECTION</p><h1>Your bag<span>.</span></h1>
    {message && <p className="inline-message">{message}</p>}
    {!items.length ? <div className="empty-state compact"><h2>Your bag is taking a break.</h2><p>Add something you love to get started.</p><Link className="dark-button" to="/shop">Continue shopping</Link></div> : <div className="cart-layout">
      <div className="cart-list">{items.map(item => <article className="cart-item" key={item.id}>
        <img src={item.product_detail.thumbnail || 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=400'} alt={item.product_detail.name} />
        <div className="cart-item-info"><h3>{item.product_detail.name}</h3><p>{item.product_detail.category}</p><div className="quantity-control"><button onClick={() => updateQuantity(item, item.quantity - 1)}><Minus size={13} /></button><span>{item.quantity}</span><button onClick={() => updateQuantity(item, item.quantity + 1)}><Plus size={13} /></button></div></div>
        <div className="cart-item-end"><strong>{peso(Number(item.product_detail.price) * item.quantity)}</strong><button className="remove-button" onClick={() => removeItem(item.id)}><Trash2 size={14} /> Remove</button></div>
      </article>)}</div>
      <aside className="order-summary"><h2>Order summary</h2><div><span>Subtotal</span><strong>{peso(total)}</strong></div><div><span>Shipping</span><span>Calculated later</span></div><hr /><div className="summary-total"><span>Total</span><strong>{peso(total)}</strong></div><button className="dark-button full-button" onClick={checkout} disabled={busy}>{busy ? 'Processing…' : 'Place order'}</button><p>Demo checkout creates an order and updates product stock.</p></aside>
    </div>}
  </section>;
}
