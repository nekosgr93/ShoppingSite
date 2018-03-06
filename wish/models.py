from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.


class WishList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wish_list')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='wish_list')

    def __str__(self):
        return self.user.username + ' ' + self.product.title
