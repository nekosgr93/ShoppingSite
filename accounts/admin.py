from django.contrib import admin
from .models import UserProfiles, UserAddress
# Register your models here.
admin.site.register(UserProfiles)
admin.site.register(UserAddress)
