from django.db import models
from django.contrib.auth.models import User
import random
import os
from django.urls import reverse
from django.utils.text import slugify
from django.core.validators import MinValueValidator

# Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    return "products/{username}/{product}/{filename}{ext}".format(username=instance.user.username,
                                                                  product=new_filename,
                                                                  filename=new_filename,
                                                                  ext =ext)


class Category(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='product')
    title = models.CharField(max_length=20)
    slug = models.SlugField(blank=True, unique=True)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    image = models.ImageField(upload_to=upload_image_path, blank=True)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(0)])
    in_stock = models.BooleanField(default=True)
    category = models.OneToOneField(Category, blank=True, null=True)
    description = models.TextField()
    star_rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.title)
        if self.quantity <= 0:
            # If the quantity is under 0, the product is sold out
            self.in_stock = False
        else:
            self.in_stock = True
        super(Product, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('products:product_detail', kwargs={"username": self.user.username, "slug": self.slug})

    def total_star_rating(self):
        comment_star_list = self.comment.all()
        rating = []
        for comment in comment_star_list:
            if comment.star_rating != 0:
                rating.append(comment.star_rating)
        print(rating)
        total = int(sum(rating)/len(rating))
        print(total)
        self.star_rating = total
        self.save()

    def star_rating_list(self):
        star_list = []
        for star in range(0, self.star_rating):
            star_list.append('on')
        for black_star in range(0, 5-self.star_rating):
            star_list.append('off')
        return star_list
