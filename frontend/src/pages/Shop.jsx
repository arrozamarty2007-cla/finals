import { useEffect, useMemo, useState } from 'react';
import { ArrowDown, Search } from 'lucide-react';
import { useOutletContext } from 'react-router-dom';
import { apiRequest } from '../api/config';
import { useAuth } from '../context/AuthContext';
import ProductCard from '../components/products/ProductCard';

const categories = ['All', 'Tops', 'Bottoms', 'Outerwear'];
const sampleProducts = [
  { id: 1, name: 'The Everyday Tee', description: 'A relaxed cotton t-shirt made for daily wear.', price: '790.00', stock: 30, category: 'Tops', thumbnail: 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=900' },
  { id: 2, name: 'Soft Knit Polo', description: 'A refined knit polo with a clean silhouette.', price: '1190.00', stock: 18, category: 'Tops', thumbnail: 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=900' },
  { id: 3, name: 'Relaxed Linen Shirt', description: 'A lightweight layer for warm, easy days.', price: '1390.00', stock: 20, category: 'Tops', thumbnail: 'https://images.unsplash.com/photo-1603252109303-2751441dd157?w=900' },
  { id: 4, name: 'Straight Cut Denim', description: 'Classic straight-leg denim with a comfortable fit.', price: '1690.00', stock: 14, category: 'Bottoms', thumbnail: 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=900' },
  { id: 5, name: 'Tailored Wide Pants', description: 'A modern wide-leg shape with a tailored finish.', price: '1590.00', stock: 16, category: 'Bottoms', thumbnail: 'https://images.unsplash.com/photo-1506629905607-d9b1c5f3e6f4?w=900' },
  { id: 6, name: 'Everyday Overshirt', description: 'An easy overshirt that works across seasons.', price: '1890.00', stock: 10, category: 'Outerwear', thumbnail: 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=900' },
];

export default function Shop() {
  const [products, setProducts] = useState(sampleProducts);
  const [category, setCategory] = useState('All');
  const [search, setSearch] = useState('');
  const [notice, setNotice] = useState('');
  const { user } = useAuth();
  const { openLogin } = useOutletContext();

  useEffect(() => { apiRequest('/products/').then(setProducts).catch(() => {}); }, []);
  const filteredProducts = useMemo(() => products.filter(product =>
    (category === 'All' || product.category === category) &&
    `${product.name} ${product.description}`.toLowerCase().includes(search.toLowerCase())
  ), [products, category, search]);

  async function addToBag(product) {
    if (!user) { openLogin(); return; }
    try {
      await apiRequest('/cart/items/', { method: 'POST', body: JSON.stringify({ product: product.id, quantity: 1 }) });
      setNotice(`${product.name} added to your bag.`);
    } catch (error) { setNotice(error.message); }
    window.setTimeout(() => setNotice(''), 2800);
  }

  return (
    <>
      <section className="hero-section">
        <div className="hero-content">
          <p className="eyebrow">THE EVERYDAY COLLECTION — 2026</p>
          <h1>Less, but<br /><em>better.</em></h1>
          <p className="hero-description">Thoughtful pieces. Effortless days.<br />A considered wardrobe starts here.</p>
          <a className="dark-button" href="#collection">Explore collection <ArrowDown size={15} /></a>
        </div>
        <div className="hero-photo">
          <img src="https://images.unsplash.com/photo-1483985988355-763728e1935b?w=1400" alt="Minimal everyday fashion collection" />
          <span className="photo-caption">FORM / FUNCTION<br />EST. MMXXVI</span>
          <span className="photo-index">01 — 06</span>
        </div>
      </section>

      <section className="intro-line"><span>DESIGNED FOR REAL LIFE</span><p>Modern essentials, made to move with you.</p><span>MANILA · PH</span></section>

      <section className="collection-section" id="collection">
        <div className="section-heading">
          <div><p className="eyebrow">CURATED FOR YOU</p><h2>The collection<span>.</span></h2></div>
          <label className="search-field"><Search size={17} /><input value={search} onChange={event => setSearch(event.target.value)} placeholder="Find your piece" /></label>
        </div>
        <div className="filter-row">
          <div className="category-filters">{categories.map(item => <button key={item} className={category === item ? 'filter-active' : ''} onClick={() => setCategory(item)}>{item}</button>)}</div>
          <span>{filteredProducts.length} PIECES</span>
        </div>
        <div className="product-grid">{filteredProducts.map(product => <ProductCard key={product.id} product={product} onAdd={addToBag} />)}</div>
        {!filteredProducts.length && <p className="no-products">No pieces found. Try another search.</p>}
      </section>

      <section className="brand-note"><p className="eyebrow">OUR PHILOSOPHY</p><h2>Wear what feels<br /><em>like you.</em></h2><p>A good wardrobe isn't about having more. It's about choosing pieces you'll reach for, again and again.</p><span>THREADLINE — EVERYDAY, INTENTIONALLY.</span></section>
      {notice && <div className="toast-message">{notice}</div>}
    </>
  );
}
