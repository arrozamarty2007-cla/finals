from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BaseUser, Cart, CartProduct, Product, ProductTransaction, Transaction

admin.site.register(BaseUser, UserAdmin)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(Transaction)
admin.site.register(ProductTransaction)
