from django.db import transaction as db_transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BaseUser, Cart, CartProduct, Product, ProductTransaction, Transaction
from .serializers import (
    BaseUserSerializer, CartProductSerializer, LoginSerializer,
    ProductSerializer, TransactionSerializer,
)


class RegisterAPIView(generics.CreateAPIView):
    queryset = BaseUser.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': BaseUserSerializer(user).data}, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user': BaseUserSerializer(user).data})


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(BaseUserSerializer(request.user).data)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        products = Product.objects.filter(is_active=True)
        search = self.request.query_params.get('search', '').strip()
        category = self.request.query_params.get('category', '').strip()
        if search:
            products = products.filter(Q(name__icontains=search) | Q(description__icontains=search))
        if category and category.lower() != 'all':
            category_sku_prefixes = {
                'tops': 'TOP',
                'bottoms': 'BTM',
                'outerwear': 'OUT',
            }
            sku_prefix = category_sku_prefixes.get(category.lower())
            if sku_prefix is None:
                return Product.objects.none()
            products = products.filter(sku__icontains=sku_prefix)
        return products.order_by('-created_at')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'HEAD', 'OPTIONS']:
            return [AllowAny()]
        return [IsAuthenticated()]


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_cart(self, user):
        cart = Cart.objects.filter(owner=user).order_by('-created_at').first()
        if cart is None:
            cart = Cart.objects.create(owner=user)
        return cart

    def get(self, request):
        cart = self.get_cart(request.user)
        items = cart.cart_products.select_related('product')
        return Response(CartProductSerializer(items, many=True).data)

    def post(self, request):
        product = get_object_or_404(Product, pk=request.data.get('product'), is_active=True)
        try:
            quantity = int(request.data.get('quantity', 1))
        except (TypeError, ValueError):
            return Response({'detail': 'Quantity must be a number.'}, status=400)
        if quantity < 1:
            return Response({'detail': 'Quantity must be at least one.'}, status=400)
        cart = self.get_cart(request.user)
        item = CartProduct.objects.filter(cart=cart, product=product).first()
        new_quantity = quantity + (item.quantity if item else 0)
        if new_quantity > product.stock:
            return Response({'detail': 'There is not enough stock for this item.'}, status=400)
        if item:
            item.quantity = new_quantity
            item.save()
        else:
            item = CartProduct.objects.create(cart=cart, product=product, quantity=quantity)
        return Response(CartProductSerializer(item).data, status=status.HTTP_201_CREATED)


class CartItemAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_item(self, request, pk):
        return get_object_or_404(CartProduct, pk=pk, cart__owner=request.user)

    def patch(self, request, pk):
        item = self.get_item(request, pk)
        try:
            quantity = int(request.data.get('quantity', item.quantity))
        except (TypeError, ValueError):
            return Response({'detail': 'Quantity must be a number.'}, status=400)
        if quantity < 1 or quantity > item.product.stock:
            return Response({'detail': 'Please choose an available quantity.'}, status=400)
        item.quantity = quantity
        item.save()
        return Response(CartProductSerializer(item).data)

    def delete(self, request, pk):
        self.get_item(request, pk).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @db_transaction.atomic
    def post(self, request):
        cart = Cart.objects.filter(owner=request.user).order_by('-created_at').first()
        if cart is None:
            return Response({'detail': 'Your cart is empty.'}, status=400)
        cart_items = list(cart.cart_products.select_related('product'))
        if not cart_items:
            return Response({'detail': 'Your cart is empty.'}, status=400)
        for cart_item in cart_items:
            if cart_item.quantity > cart_item.product.stock:
                return Response({'detail': f'Not enough stock for {cart_item.product.name}.'}, status=400)
        order = Transaction.objects.create(buyer=request.user)
        for cart_item in cart_items:
            product = cart_item.product
            ProductTransaction.objects.create(
                transaction=order,
                item=product,
                quantity=cart_item.quantity,
            )
            product.stock -= cart_item.quantity
            product.save(update_fields=['stock', 'updated_at'])
        cart.cart_products.all().delete()
        return Response(TransactionSerializer(order).data, status=status.HTTP_201_CREATED)


class TransactionListAPIView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(buyer=self.request.user).prefetch_related('product_transactions__item').order_by('-created_at')
