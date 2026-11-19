from django.core.management.base import BaseCommand
from accounts.models import Product

SAMPLE_PRODUCTS = [
    ('The Everyday Tee', 'A relaxed cotton t-shirt made for daily wear.', 'TL-TOP-001', '790.00', 30, 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=900'),
    ('Soft Knit Polo', 'A refined knit polo with a clean silhouette.', 'TL-TOP-002', '1190.00', 18, 'https://images.unsplash.com/photo-1618354691373-d851c5c3a990?w=900'),
    ('Relaxed Linen Shirt', 'A lightweight layer for warm, easy days.', 'TL-TOP-003', '1390.00', 20, 'https://images.unsplash.com/photo-1603252109303-2751441dd157?w=900'),
    ('Straight Cut Denim', 'Classic straight-leg denim with a comfortable fit.', 'TL-BTM-001', '1690.00', 14, 'https://images.unsplash.com/photo-1542272604-787c3835535d?w=900'),
    ('Tailored Wide Pants', 'A modern wide-leg shape with a tailored finish.', 'TL-BTM-002', '1590.00', 16, 'https://images.unsplash.com/photo-1506629905607-d9b1c5f3e6f4?w=900'),
    ('Everyday Overshirt', 'An easy overshirt that works across seasons.', 'TL-OUT-001', '1890.00', 10, 'https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=900'),
]


class Command(BaseCommand):
    help = 'Add sample clothing products to the shop.'

    def handle(self, *args, **options):
        for name, description, sku, price, stock, thumbnail in SAMPLE_PRODUCTS:
            Product.objects.update_or_create(
                sku=sku,
                defaults={
                    'name': name,
                    'description': description,
                    'price': price,
                    'stock': stock,
                    'thumbnail': thumbnail,
                    'is_active': True,
                },
            )
        self.stdout.write(self.style.SUCCESS('Sample clothing products are ready.'))
