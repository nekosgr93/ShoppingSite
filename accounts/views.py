from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

from .models import UserAddress, UserProfiles
from . import forms

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


class UserProfile(DetailView):
    model = UserProfiles
    template_name = 'accounts/profile_list.html'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return get_object_or_404(User, username=username).userprofiles


class UpdateProfile(LoginRequiredMixin, UpdateView):
    form_class = forms.ProfileForm
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/profile_form.html'

    def get_object(self, queryset=None):
        user = self.request.user
        return get_object_or_404(UserProfiles, user=user)


class CreateAddress(LoginRequiredMixin, CreateView):
    form_class = forms.AddressForm
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/address_form.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateAddress(LoginRequiredMixin, UpdateView):
    form_class = forms.AddressForm
    login_url = reverse_lazy('accounts:login')
    template_name = 'accounts/address_form.html'

    def get_object(self, queryset=None):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserAddress, user=user, id=pk)


class DeleteAddress(LoginRequiredMixin, DeleteView):
    login_url = 'accounts/login/'
    model = UserAddress

    def get_object(self, queryset=None):
        user = self.request.user
        pk = self.kwargs.get('pk')
        return get_object_or_404(UserAddress, user=user, id=pk)

    def get_success_url(self):
        return reverse_lazy('accounts:user_address', kwargs={'username': self.request.user.username})


class AddressList(ListView):
    model = UserAddress
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