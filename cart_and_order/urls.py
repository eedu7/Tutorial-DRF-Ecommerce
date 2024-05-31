from django.urls import path

from cart_and_order.views import (
    ProductAPIView,
    CartAPIView,
    OrderAPIView,
    CartItemAPIView,
    ShippingAddressAPIView,
)

urlpatterns = [
    path("", ProductAPIView.as_view(), name="product-api"),
    path("cart/", CartAPIView().as_view(), name="cart-api"),
    path("order/", OrderAPIView.as_view(), name="order-api"),
    path("cart/item/", CartItemAPIView.as_view(), name="cart-item-api"),
    path(
        "shipping-address/",
        ShippingAddressAPIView.as_view(),
        name="shipping-address-api",
    ),
]
