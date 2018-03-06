from django.shortcuts import render, redirect, get_object_or_404
# from .cart import create_or_retrieve_cart
from .forms import Product_Add_Form
from products.models import Product
from .models import Cart, CartItem
from .cart import Anon_User_Cart, Auth_User_Cart
from django.views.decorators.http import require_POST
from decimal import Decimal

# Create your views here.


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





# def cart_detail(request):
#     cart = create_or_retrieve_cart(request)
#     cart_items = cart.get_cart_items()
#     return render(request, 'carts/cart_detail.html', {'cart': cart_items})
#
#
# def add_to_cart(request, product_id):
#     if request.method == 'POST':
#         cart = create_or_retrieve_cart(request)
#         product = Product.objects.get(id=product_id)
#         quantity_form = Product_Add_Form(request.POST)
#         if quantity_form.is_valid():
#             quantity = quantity_form.cleaned_data['quantity']
#             item = CartItem()
#             item.cart = cart
#             item.product = product
#             item.price = product.price
#             item.quantity = quantity
#             item.save()
#             cart.calculate_total()
#     return redirect('carts:cart_detail')

