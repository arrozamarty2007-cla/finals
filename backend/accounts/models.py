from django.contrib.auth.models import AbstractUser
from django.db import models


class BaseUser(AbstractUser):
    id = None
    UniqueID = models.BigAutoField(primary_key=True)
    """Customer account. This is the base_users table in the ERD."""
    email = models.EmailField(unique=True)
    middle_name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    avatar = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'base_users'

    def __str__(self):
        return self.username


class Product(models.Model):
    UniqueID = models.BigAutoField(primary_key=True)
    """Clothing products available in the shop."""
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'

    def __str__(self):
        return self.name


class Cart(models.Model):
    UniqueID = models.BigAutoField(primary_key=True)
    """A shopping cart owned by one user."""
    owner = models.ForeignKey(BaseUser, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'

    def __str__(self):
        return f'Cart #{self.pk} - {self.owner.username}'


class CartProduct(models.Model):
    UniqueID = models.BigAutoField(primary_key=True)
    """A product and quantity saved inside a cart."""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_products')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='cart_products')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'cart_products'
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product'], name='one_product_per_cart')
        ]


class Transaction(models.Model):
    UniqueID = models.BigAutoField(primary_key=True)
    """An order placed by a buyer."""
    buyer = models.ForeignKey(BaseUser, on_delete=models.PROTECT, related_name='transactions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return f'Order #{self.pk}'


class ProductTransaction(models.Model):
    UniqueID = models.BigAutoField(primary_key=True)
    """Products and quantities saved as lines in an order."""
    item = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='product_transactions')
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE, related_name='product_transactions')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'product_transactions'
