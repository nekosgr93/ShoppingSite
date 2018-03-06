from django.db import models
from django.contrib.auth.models import User
from products.models import Product
# Create your models here.

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comment')
    title = models.CharField(max_length=20)
    content = models.TextField(max_length=200)
    star_rating = models.SmallIntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def star_rating_list(self):
        star_list = []
        for star in range(0, self.star_rating):
            star_list.append('on')
        for black_star in range(0, 5-self.star_rating):
            star_list.append('off')
        return star_list
