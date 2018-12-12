from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .cart import Anon_User_Cart, Auth_User_Cart
from products.models import Product


def cart_detail(request):
    if request.user.is_authenticated():
        cart = Auth_User_Cart(request)
        item_list = cart.get_cart_item
    else:
        cart = Anon_User_Cart(request)
        item_list = cart.get_cart_item
    return render(request, 'carts/cart_detail.html', {'cart': cart, 'item_list': item_list})


@require_POST
def add_to_cart(request, product_id):
    if 'add_to_cart' in request.POST:
        product = get_object_or_404(Product, id=product_id)
        quantity = int(request.POST.get('quantity'))
        if request.user.is_authenticated():
            cart = Auth_User_Cart(request)
            cart.add(product, quantity)
        else:
            cart = Anon_User_Cart(request)
            cart.add(product, quantity)
    return redirect('carts:cart_detail')


@require_POST
def remove_form_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated():
        cart = Auth_User_Cart(request)
        cart.remove(product)
    else:
        cart = Anon_User_Cart(request)
        cart.remove(product)
    return redirect('carts:cart_detail')
