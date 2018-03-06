from django.db import models
from django.contrib.auth.models import User
from carts.models import Cart, CartItem
from accounts.models import UserAddress
# Create your models here.


class Order(models.Model):
    COUNTRY = [('China', 'China'),
               ('Canada', 'Canada'),
               ('Japan', 'Japan'),
               ('United Kingdom', 'United Kingdom'),
               ('United States', 'United States'),
               ('Taiwan', 'Taiwan')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='order')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='order')
    address = models.ForeignKey(UserAddress, on_delete=models.CASCADE, related_name='order', null=True, blank=False)
    shipping_full_name = models.CharField(max_length=100, default='', null=True)
    shipping_postal_code = models.CharField(max_length=16, default='', null=True)
    shipping_country = models.CharField(max_length=50, choices=COUNTRY, null=True)
    shipping_address1 = models.CharField(max_length=100, default='', null=True)
    shipping_address2 = models.CharField(max_length=100, default='', null=True)
    shipping_phone_number = models.CharField(max_length=15, default='', null=True)
    paid = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
