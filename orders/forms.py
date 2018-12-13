from django import forms
from .models import Order


class User_address_choice_form(forms.Form):
    address_id = forms.IntegerField(required=True)


class New_shipping_address_form(forms.ModelForm):
    shipping_address1 = forms.CharField(max_length=100, label='address1',
                                        widget=forms.TextInput(attrs={'placeholder': 'Street and Number'}))
    shipping_address2 = forms.CharField(max_length=100, label='address2',
                                        widget=forms.TextInput(
                                            attrs={'placeholder': 'Apartment, suite, unit, building, floor, etc...'}))

    class Meta:
        model = Order
        fields = ('shipping_full_name',
                  'shipping_postal_code',
                  'shipping_address1',
                  'shipping_address2',
                  'shipping_country',
                  'shipping_phone_number')
