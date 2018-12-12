from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from carts.forms import Product_Add_Form

from . import forms
from .models import Product


class CreateProduct(LoginRequiredMixin, CreateView):
    form_class = forms.ProductForm
    login_url = 'accounts/login/'
    template_name = "products/product_form.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class UpdateProduct(LoginRequiredMixin, UpdateView):
    form_class = forms.ProductForm
    login_url = 'accounts/login/'
    template_name = "products/product_form.html"

    def get_object(self, queryset=None):
        user = self.request.user
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, user=user, slug=slug)


class DeleteProduct(LoginRequiredMixin, DeleteView):
    login_url = 'accounts/login/'

    def get_object(self, queryset=None):
        user = self.request.user
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, user=user, slug=slug)

    def get_success_url(self):
        return reverse_lazy('products:product_list', kwargs={'username': self.request.user})


class ProductList(ListView):
    context_object_name = "product"
    template_name = "products/product_list.html"

    def get_queryset(self):
        self.user_product = User.objects.prefetch_related('product').get(username=self.kwargs.get("username"))
        return self.user_product.product.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_user"] = self.user_product
        return context


class ProductDetail(DetailView):
    select_related = ('user',)
    template_name = "products/product_detail.html"

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        user = get_object_or_404(User, username=username)
        slug = self.kwargs.get('slug')
        return get_object_or_404(Product, user=user, slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        context["form"] = Product_Add_Form(product.quantity)
        context['comment_list'] = product.comment.all()
        return context
