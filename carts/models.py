from django.db import models
from django.contrib.auth.models import User
from products.models import Product


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='cart')
    total = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    activate = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

    def get_cart_items(self):
        return self.cartitem.all()

    def calculate_total(self):
        items = self.get_cart_items()
        self.total = sum(item.subtotal for item in items)
        self.save()

    def paid_cart(self):
        """If the order is paid, set the cart to inactivate and reduce the product quantity"""
        items = self.get_cart_items()
        for item in items:
            item.reduce()
        self.activate = False
        self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartitem')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='cartitem')
    price = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    subtotal = models.DecimalField(blank=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.product.title

    def save(self, *args, **kwargs):
        self.subtotal = (self.price*self.quantity)
        super().save(*args, **kwargs)

    def reduce(self):
        """If the product has been bought and finished the payment,
        reduce the quantity of the product"""
        self.product.quantity -= self.quantity
        self.product.save()
