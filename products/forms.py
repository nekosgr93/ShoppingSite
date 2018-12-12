from django.forms import ModelForm
from . import models


class ProductForm(ModelForm):
    class Meta:
        model = models.Product
        fields = ('title', 'image', 'price', 'quantity', 'category', 'description')
