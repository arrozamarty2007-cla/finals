from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework import serializers
from .models import BaseUser, CartProduct, Product, ProductTransaction, Transaction


class BaseUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='UniqueID', read_only=True)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = BaseUser
        fields = [
            'id', 'username', 'email', 'password', 'confirm_password',
            'first_name', 'middle_name', 'last_name', 'gender', 'avatar',
            'is_active', 'date_joined',
        ]
        read_only_fields = ['id', 'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, attrs):
        password = attrs.get('password')
        confirm = attrs.pop('confirm_password', None)
        if password:
            if password != confirm:
                raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})
            try:
                validate_password(password, user=self.instance)
            except DjangoValidationError as error:
                raise serializers.ValidationError({'password': error.messages}) from error
        return attrs

    def create(self, validated_data):
        return BaseUser.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        user = authenticate(
            request=self.context.get('request'),
            username=attrs['username'],
            password=attrs['password'],
        )
        if user is None:
            raise serializers.ValidationError({'detail': 'Invalid username or password.'})
        attrs['user'] = user
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='UniqueID', read_only=True)
    category = serializers.SerializerMethodField()

    def get_category(self, obj):
        sku = obj.sku.upper()
        if 'TOP' in sku:
            return 'Tops'
        if 'BTM' in sku:
            return 'Bottoms'
        if 'OUT' in sku:
            return 'Outerwear'
        return 'Clothing'

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'sku', 'price', 'stock',
            'thumbnail', 'category', 'is_active', 'created_at', 'updated_at',
        ]


class CartProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='UniqueID', read_only=True)
    product_detail = ProductSerializer(source='product', read_only=True)
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartProduct
        fields = ['id', 'cart', 'product', 'product_detail', 'quantity', 'line_total']
        read_only_fields = ['id', 'cart', 'product_detail', 'line_total']

    def get_line_total(self, obj):
        return str(obj.product.price * obj.quantity)


class ProductTransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='UniqueID', read_only=True)
    product_detail = ProductSerializer(source='item', read_only=True)
    unit_price = serializers.SerializerMethodField()

    def get_unit_price(self, obj):
        return str(obj.item.price)

    class Meta:
        model = ProductTransaction
        fields = ['id', 'item', 'product_detail', 'quantity', 'unit_price']


class TransactionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='UniqueID', read_only=True)
    product_transactions = ProductTransactionSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        return 'PLACED'

    class Meta:
        model = Transaction
        fields = ['id', 'buyer', 'created_at', 'status', 'product_transactions', 'total']

    def get_total(self, obj):
        total = sum((line.item.price * line.quantity for line in obj.product_transactions.select_related('item').all()), start=0)
        return str(total)
