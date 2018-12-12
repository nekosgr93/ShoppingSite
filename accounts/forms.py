from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import UserProfiles, UserAddress


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfiles
        fields = ("bio", "profile_pic")


class AddressForm(forms.ModelForm):
    address1 = forms.CharField(max_length=100, label='address1',
                               widget=forms.TextInput(attrs={'placeholder': 'Street and Number'}))
    address2 = forms.CharField(max_length=100, label='address2',
                               widget=forms.TextInput(
                                                attrs={
                                                    'placeholder': 'Apartment, suite, unit, building, floor, etc...'}
                                            ))

    class Meta:
        model = UserAddress
        fields = ('full_name', 'postal_code', 'address1', 'address2', 'country', 'phone_number')
