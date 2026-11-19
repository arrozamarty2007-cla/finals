from decimal import Decimal

from django.db import IntegrityError, transaction
from django.test import TestCase

from .models import (
    BaseUser,
    Cart,
    CartProduct,
    Product,
    ProductTransaction,
    Transaction,
)


class StoreModelTests(TestCase):
    def setUp(self):
        self.user = BaseUser.objects.create_user(
            username="buyer",
            password="test-password",
        )
        self.product = Product.objects.create(
            name="Sample product",
            sku="SAMPLE-001",
            price=Decimal("12.50"),
            stock=5,
        )

    def test_cart_and_transaction_relationships(self):
        cart = Cart.objects.create(owner=self.user)
        cart_item = CartProduct.objects.create(cart=cart, product=self.product)
        sale = Transaction.objects.create(buyer=self.user)
        sale_item = ProductTransaction.objects.create(
            transaction=sale,
            item=self.product,
            quantity=2,
        )

        self.assertEqual(cart_item.pk.version, 4)
        self.assertEqual(cart.items.count(), 1)
        self.assertEqual(sale.product_transactions.get(), sale_item)
        self.assertEqual(self.user.transactions.get(), sale)
        self.assertEqual(sale_item.item, self.product)
        self.assertTrue(self.user.check_password("test-password"))

    def test_cart_cannot_contain_duplicate_product_rows(self):
        cart = Cart.objects.create(owner=self.user)
        CartProduct.objects.create(cart=cart, product=self.product)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                CartProduct.objects.create(cart=cart, product=self.product)
