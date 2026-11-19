from django.contrib import admin

from .models import BaseUser, Cart, CartProduct, Product, ProductTransaction, Transaction


@admin.register(BaseUser)
class BaseUserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")
    readonly_fields = ("password", "last_login")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "price", "stock", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "sku")


admin.site.register((Cart, CartProduct, Transaction, ProductTransaction))
