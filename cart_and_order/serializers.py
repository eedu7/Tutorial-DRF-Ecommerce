from django.contrib.auth import get_user_model
from rest_framework import serializers

from cart_and_order.models import Product, ShippingAddress, CartItems, Cart, Order

User = get_user_model()


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "product_name", "product_price", "product_stock"]

    def create(self, validated_data):
        product, created = Product.objects.get_or_create(
            product_name=validated_data["product_name"], defaults=validated_data
        )
        if not created:
            product.product_stock += validated_data["product_stock"]
            product.save()
        return product


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = ["address", "second_address", "city"]


class ProductInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["product_name", "product_price"]


class CartItemsSerializer(serializers.ModelSerializer):
    cart_product_info = serializers.SerializerMethodField()

    class Meta:
        model = CartItems
        fields = [
            "cart",
            "cart_product",
            "cart_product_quantity",
            "cart_product_info"
        ]
        extra_kwargs = {
            "cart": {"write_only": True},
            "cart_product": {"write_only": True},
        }

    def get_cart_product_info(self, obj):
        return ProductInfoSerializer(obj.cart_product).data

    def create(self, validated_data):
        user = self.context["request"].user
        cart_product = validated_data.get("cart_product")
        cart_product_quantity = validated_data.get("cart_product_quantity")

        # Check if there is a pending cart for the user
        cart, created = Cart.objects.get_or_create(user=user, cart_status="PENDING")

        if not created:
            # If the cart already exists and is pending, just add the item
            cart_item, created = CartItems.objects.get_or_create(
                cart=cart, cart_product=cart_product
            )
            if not created:
                # If the item already exists in the Cart, update the quantity
                cart_item.cart_product_quantity += cart_product_quantity
                cart_item.save()
        else:
            cart_item = CartItems.objects.create(
                cart=cart,
                cart_product=cart_product,
                cart_product_quantity=cart_product_quantity,
            )
            cart_item.save()
        return cart_item


class CartSerializer(serializers.ModelSerializer):
    items = CartItemsSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "cart_status", "items"]


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    order_shipping_address = ShippingAddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["cart", "order_shipping_address"]

    def create(self, validated_data):
        user = self.context["request"].user
        cart = Cart.objects.get(user=user, cart_status="PENDING")
        shipping_address = ShippingAddress.objects.get(user=user)
        return Order.objects.create(
            user=user, cart=cart, order_shipping_address=shipping_address
        )
