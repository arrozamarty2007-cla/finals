from django.test import TestCase
from rest_framework.test import APIClient

from .models import BaseUser, Product


class AccountRegistrationTests(TestCase):
    def test_registration_creates_user_and_returns_token(self):
        response = self.client.post('/api/auth/register/', {
            'username': 'new-customer',
            'email': 'new-customer@example.com',
            'password': 'Threadline-Test-Password-58!',
            'confirm_password': 'Threadline-Test-Password-58!',
            'first_name': 'New',
            'last_name': 'Customer',
        }, format='json')

        self.assertEqual(response.status_code, 201, response.data)
        self.assertTrue(response.data['token'])
        self.assertEqual(response.data['user']['username'], 'new-customer')
        user = BaseUser.objects.get(username='new-customer')
        self.assertTrue(user.check_password('Threadline-Test-Password-58!'))


class ProductCategoryFilterTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.products = [
            Product.objects.create(name='Tee', sku='TL-TOP-001', price='10.00', stock=2),
            Product.objects.create(name='Jeans', sku='TL-BTM-001', price='20.00', stock=2),
            Product.objects.create(name='Jacket', sku='TL-OUT-001', price='30.00', stock=2),
        ]

    def test_category_filters_products_by_sku(self):
        for category, product in zip(('Tops', 'Bottoms', 'Outerwear'), self.products):
            with self.subTest(category=category):
                response = self.client.get('/api/products/', {'category': category})

                self.assertEqual(response.status_code, 200)
                self.assertEqual([item['id'] for item in response.data], [product.pk])

    def test_unknown_category_returns_no_products(self):
        response = self.client.get('/api/products/', {'category': 'Accessories'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])
