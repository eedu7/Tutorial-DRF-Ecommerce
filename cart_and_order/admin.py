from django.contrib import admin

from cart_and_order.models import Product, ShippingAddress, Cart, CartItems, Order


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id", "product_name", "product_stock", "product_price"]


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "address",
        "city",
    ]


@admin.register(CartItems)
class CartItemsAdmin(admin.ModelAdmin):
    list_display = ["id", "cart", "cart_product", "cart_product_quantity"]


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "user", "cart_status"]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "cart",
        "total_amount",
        "order_shipping_address",
    ]
