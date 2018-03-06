from django import forms
from products.models import Product


class Product_Add_Form(forms.Form):
    def __init__(self, quantity=1, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.quantity_chioce = [(i, str(i)) for i in range(1, quantity+1)]
        self.fields['quantity'] = forms.TypedChoiceField(
                                  choices=self.quantity_chioce,
                                  coerce=int)

