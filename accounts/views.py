from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
# from django.urls import reverse
from . import forms
from django.contrib import messages
from django.views import generic
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from braces.views import SelectRelatedMixin


# Create your views here.


def SignupView(request):
    if request.method == "POST":
        signup_form = forms.SignupForm(data=request.POST)
        if signup_form.is_valid():
            signup_form.save()
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        signup_form = forms.SignupForm()

    return render(request, 'accounts/signup.html', {'form': signup_form})


def User_profile(request, username):
    profiles = get_object_or_404(User, username=username).userprofiles
    return render(request, 'accounts/profile_list.html', {'profiles': profiles})


@login_required
def edit_profile(request, username):
    instance = User.objects.get(username=username).userprofiles
    if request.method == "POST":
        form = forms.ProfileForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('accounts:profiles', username=username)
    else:
        form = forms.ProfileForm(instance=instance)
    return render(request, 'accounts/profile_edit.html', {'form': form})


@login_required
def create_address(request, username):
    if request.method == "POST":
        address_form = forms.AddressForm(request.POST)
        if address_form.is_valid():
            form = address_form.save(commit=False)
            user = User.objects.get(username=request.user)
            form.user = user
            form.save()
            return redirect('accounts:user_address', username=username)
    else:
        address_form = forms.AddressForm()
    return render(request, 'accounts/create_or_edit_address.html', {'form': address_form})


class UpdateAddress(LoginRequiredMixin, generic.UpdateView):
    model = models.UserAddress
    login_url = 'accounts/login/'
    redirect_field_name = 'accounts/address_list.html'
    select_related = ('user',)
    form_class = forms.AddressForm
    template_name = "accounts/create_or_edit_address.html"


class DeleteAddress(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    login_url = 'accounts/login/'
    model = models.UserAddress
    select_related = ('user',)

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def get_success_url(self):
        return reverse_lazy('accounts:user_address', kwargs={'username': self.request.user.username})



# def AddressList(request, username):
#     address_list = User.objects.get(username=username).useraddress.all()
#     print(address_list)
#     return render(request, 'accounts/address_list.html', {'address_list': address_list})


class AddressList(generic.ListView):
    model = models.UserAddress
    context_object_name = 'address_list'
    template_name = 'accounts/address_list.html'

    def get_queryset(self):
        self.user_address = User.objects.prefetch_related('useraddress').get(username=self.kwargs.get("username"))
        return self.user_address.useraddress.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["address_user"] = self.user_address
        return context



















###### Manually login/logout view ######

# def user_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('welcome'))
#             else:
#                 return HttpResponseRedirect(reverse('login'))
#         else:
#             return HttpResponseRedirect(reverse('login'))
#     else:
#         return render(request, 'accounts/login.html')
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('index'))