from django.urls import path
from .views import (
    CartAPIView, CartItemAPIView, CheckoutAPIView, LoginAPIView,
    LogoutAPIView, MeAPIView, ProductDetailAPIView, ProductListCreateAPIView,
    RegisterAPIView, TransactionListAPIView,
)

urlpatterns = [
    path('auth/register/', RegisterAPIView.as_view(), name='register'),
    path('auth/login/', LoginAPIView.as_view(), name='login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='logout'),
    path('auth/me/', MeAPIView.as_view(), name='me'),
    path('products/', ProductListCreateAPIView.as_view(), name='products'),
    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cart/items/', CartAPIView.as_view(), name='cart-items'),
    path('cart/items/<int:pk>/', CartItemAPIView.as_view(), name='cart-item'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('transactions/', TransactionListAPIView.as_view(), name='transactions'),
]
