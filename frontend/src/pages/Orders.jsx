import { useEffect, useState } from 'react';
import { Link, useLocation, useOutletContext } from 'react-router-dom';
import { PackageCheck } from 'lucide-react';
import { apiRequest } from '../api/config';
import { useAuth } from '../context/AuthContext';

const peso = value => `₱${Number(value || 0).toLocaleString('en-PH', { minimumFractionDigits: 2 })}`;

export default function Orders() {
  const [orders, setOrders] = useState([]);
  const [error, setError] = useState('');
  const { user } = useAuth();
  const { openLogin } = useOutletContext();
  const location = useLocation();

  useEffect(() => {
    if (user) apiRequest('/transactions/').then(setOrders).catch(err => setError(err.message));
    else setOrders([]);
  }, [user]);

  if (!user) return <section className="empty-state"><p className="eyebrow">YOUR THREADLINE</p><h1>Order history.</h1><p>Sign in to view your orders.</p><button className="dark-button" onClick={openLogin}>Sign in</button></section>;

  return <section className="inner-page orders-page"><p className="eyebrow">YOUR THREADLINE</p><h1>Order history<span>.</span></h1>
    {location.state?.justOrdered && <p className="success-message"><PackageCheck size={17} /> Your order has been placed successfully.</p>}
    {error && <p className="inline-message">{error}</p>}
    {!orders.length ? <div className="empty-state compact"><h2>No orders yet.</h2><p>Your next favorite piece is waiting.</p><Link className="dark-button" to="/shop">Explore the collection</Link></div> : <div className="orders-list">{orders.map(order => <article className="order-card" key={order.id}><div className="order-top"><div><span>ORDER #{order.id}</span><p>{new Date(order.created_at).toLocaleString()}</p></div><b className="status-pill">{order.status}</b></div>
      {order.product_transactions.map(line => <div className="order-product" key={line.id}><img src={line.product_detail.thumbnail || 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=300'} alt="" /><div><h3>{line.product_detail.name}</h3><p>Qty: {line.quantity} · {peso(line.unit_price)} each</p></div><strong>{peso(Number(line.unit_price) * line.quantity)}</strong></div>)}
      <div className="order-total"><span>Order total</span><strong>{peso(order.total)}</strong></div></article>)}</div>}
  </section>;
}
