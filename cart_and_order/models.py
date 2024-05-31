from django.contrib.auth.models import User, AbstractUser
from django.db import models, transaction

# Create your models here.

CART_STATUS = (("ORDERED", "Ordered"), ("PENDING", "Pending"))


class Product(models.Model):
    product_name = models.CharField(max_length=255)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name


class ShippingAddress(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.TextField()
    second_address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.user.username


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_status = models.CharField(
        max_length=15, choices=CART_STATUS, default="PENDING"
    )

    def __str__(self):
        return f"{self.pk}_{self.user.username}_Cart"


class CartItems(models.Model):
    cart_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart_product_quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    def total_amount(self):
        return self.cart_product_quantity * self.cart_product.product_price

    def __str__(self):
        return (
            f"{self.cart.pk}_{self.cart.user.username}_{self.cart_product.product_name}"
        )


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart")

    order_shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.CASCADE, related_name="shipping_address"
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}_{self.created_at}"

    def save(self, *args, **kwargs):
        with transaction.atomic():
            cart = self.cart
            self.total_amount = 0

            for cart_item in cart.items.all():
                self.total_amount += cart_item.total_amount()
                product = cart_item.cart_product
                if product.product_stock < cart_item.cart_product_quantity:
                    raise ValueError("Not enough stock")
                product.product_stock += cart_item.cart_product_quantity
                product.save()
            cart.cart_status = "ORDERED"
            cart.save()
            super().save(*args, **kwargs)

    class Meta:
        ordering = ["created_at"]
