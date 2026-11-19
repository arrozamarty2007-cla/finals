import { Plus } from 'lucide-react';

export default function ProductCard({ product, onAdd }) {
  return (
    <article className="product-card">
      <div className="product-image-wrap">
        {product.thumbnail ? <img src={product.thumbnail} alt={product.name} loading="lazy" /> : <div className="image-placeholder">THREADLINE</div>}
        <span className="product-tag">{product.category}</span>
        <button className="add-product" onClick={() => onAdd(product)} aria-label={`Add ${product.name} to bag`}><Plus size={18} /></button>
      </div>
      <div className="product-caption">
        <div><h3>{product.name}</h3><p>{product.description}</p></div>
        <strong>₱{Number(product.price).toLocaleString('en-PH', { minimumFractionDigits: 2 })}</strong>
      </div>
    </article>
  );
}
