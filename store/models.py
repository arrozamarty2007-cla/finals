import uuid

from django.contrib.auth.base_user import (
    AbstractBaseUser,
    BaseUserManager as DjangoBaseUserManager,
)
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class UUIDModel(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        db_column="UniqueID",
    )

    class Meta:
        abstract = True


class BaseUserManager(DjangoBaseUserManager):
    def create_user(self, username, email="", password=None, **extra_fields):
        if not username:
            raise ValueError("A username is required.")

        user = self.model(
            username=username,
            email=self.normalize_email(email),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class BaseUser(UUIDModel, AbstractBaseUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    middle_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    gender = models.CharField(max_length=30, blank=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True)
    is_active = models.BooleanField(default=True)

    objects = BaseUserManager()

    USERNAME_FIELD = "username"

    class Meta:
        db_table = "base_users"


class Product(UUIDModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    stock = models.PositiveIntegerField(default=0)
    thumbnail = models.ImageField(upload_to="products/", blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products"
        constraints = [
            models.CheckConstraint(
                condition=Q(price__gte=0),
                name="product_price_non_negative",
            ),
        ]
        ordering = ["name"]

    def __str__(self):
        return self.name


class Cart(UUIDModel):
    owner = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="carts",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "carts"
        ordering = ["-updated_at"]

    def __str__(self):
        return f"Cart for {self.owner}"


class CartProduct(UUIDModel):
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="cart_entries",
    )

    class Meta:
        db_table = "cart_products"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"],
                name="unique_product_per_cart",
            ),
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="cart_product_quantity_positive",
            ),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product}"


class Transaction(UUIDModel):
    buyer = models.ForeignKey(
        BaseUser,
        on_delete=models.PROTECT,
        related_name="transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Transaction {self.pk}"


class ProductTransaction(UUIDModel):
    quantity = models.PositiveIntegerField(default=1)
    item = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name="transaction_items",
    )
    transaction = models.ForeignKey(
        Transaction,
        on_delete=models.CASCADE,
        related_name="product_transactions",
    )

    class Meta:
        db_table = "product_transactions"
        constraints = [
            models.UniqueConstraint(
                fields=["transaction", "item"],
                name="unique_product_per_transaction",
            ),
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="product_transaction_quantity_positive",
            ),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.item}"
