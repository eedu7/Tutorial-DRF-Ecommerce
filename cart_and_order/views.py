from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cart_and_order.models import Product, ShippingAddress, CartItems, Cart, Order
from cart_and_order.serializers import (
    ProductSerializer,
    ShippingAddressSerializer,
    CartItemsSerializer,
    CartSerializer,
    OrderSerializer,
)


# Create your views here.


class ProductAPIView(GenericAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        products = self.get_queryset()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN,
            )
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class ShippingAddressAPIView(GenericAPIView):
    serializer_class = ShippingAddressSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ShippingAddress.objects.all()
        return ShippingAddress.objects.filter(user=user).first()

    def get(self, request, *args, **kwargs):
        address = self.get_queryset()
        serializer = self.get_serializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartItemAPIView(GenericAPIView):
    serializer_class = CartItemsSerializer

    def get_queryset(self):
        user = self.request.user
        try:
            cart = Cart.objects.get(user=user, cart_status="PENDING")
        except Cart.DoesNotExist:
            raise ValueError({"cart": "CartItem does not exist."})
        # cart = Cart.objects.get_or_create(user=user, cart_status="PENDING")
        # return CartItems.objects.filter(cart=cart, cart__user=user)
        return CartItems.objects.filter(cart=cart)

    def get(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CartAPIView(GenericAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Cart.objects.all()
        return Cart.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        cart_items = self.get_queryset()
        serializer = self.get_serializer(cart_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderAPIView(GenericAPIView):
    # queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(user=user)

    def get(self, request, *args, **kwargs):
        order_item = self.get_queryset()
        many = not request.user.is_staff

        serializer = self.get_serializer(order_item, many=many)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer()
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
