from django.db import models
from django.contrib.auth.models import User
import random
import os
from django.urls import reverse
#Create your models here.


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(instance, filename):
    new_filename = random.randint(1, 3910209312)
    name, ext = get_filename_ext(filename)
    return "accounts/profile_pics/{username}/{filename}{ext}".format(username=instance.user.username,
                                                                filename=new_filename,
                                                                ext = ext)



class UserProfiles(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(max_length=150, blank=True)
    profile_pic = models.ImageField(upload_to=upload_image_path, blank=True)

    def __str__(self):
        return self.user.username

    def get_absolute_urls(self):
        return reverse('accounts:profiles', kwargs={'username': self.user.username})


class UserAddress(models.Model):
    COUNTRY = [('China', 'China'),
               ('Canada', 'Canada'),
               ('Japan', 'Japan'),
               ('United Kingdom', 'United Kingdom'),
               ('United States', 'United States'),
               ('Taiwan', 'Taiwan')]

    user = models.ForeignKey(User, related_name='useraddress')
    full_name = models.CharField(max_length=100, default='', blank=False)
    postal_code = models.CharField(max_length=16, default='', null=False, blank=False)
    country = models.CharField(max_length=50, choices=COUNTRY, null=False, blank=False)
    address1 = models.CharField(max_length=100, default='', null=False, blank=False)
    address2 = models.CharField(max_length=100, default='', null=False, blank=False)
    phone_number = models.CharField(max_length=15, default='', null=False, blank=False)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('accounts:user_address', kwargs={'username': self.user.username})
