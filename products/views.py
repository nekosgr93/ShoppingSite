from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from . import forms
from django.views import generic
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import SelectRelatedMixin
from django.core.urlresolvers import reverse_lazy
from carts.forms import Product_Add_Form
# Create your views here.

class CreateProduct(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    model = models.Product
    login_url = 'accounts/login/'
    redirect_field_name = 'products/product_detail.html'
    select_related = ('user',)
    form_class = forms.ProductForm
    template_name = "products/create_edit_product.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

class UpdateProduct(LoginRequiredMixin, SelectRelatedMixin, generic.UpdateView):
    model = models.Product
    login_url = 'accounts/login/'
    redirect_field_name = 'products/product_detail.html'
    select_related = ('user',)
    form_class = forms.ProductForm
    template_name = "products/create_edit_product.html"


class DeleteProduct(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Product
    login_url = 'accounts/login/'
    select_related = ('user',)


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )

    def get_success_url(self):
        return reverse_lazy('products:product_list', kwargs={'username': self.request.user.username})


class ProductList(SelectRelatedMixin, generic.ListView):
    model = models.Product
    select_related = ('user',)
    context_object_name = "product"
    template_name = "product_list.html"

    def get_queryset(self):
        self.user_product = User.objects.prefetch_related('product').get(username=self.kwargs.get("username"))
        return self.user_product.product.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["product_user"] = self.user_product
        return context




class ProductDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Product
    select_related = ('user',)
    template_name = "products/product_detail.html"


    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     product = queryset.filter(slug__iexact=self.kwargs.get("slug"))
    #     print(product)
    #     return product


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = models.Product.objects.get(slug__iexact=self.kwargs.get("slug"))
        context["form"] = Product_Add_Form(product.quantity)
        context['comment_list'] = product.comment.all()
        return context
