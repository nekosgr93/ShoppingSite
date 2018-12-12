from django.shortcuts import render, redirect
from products.models import Product
from .models import WishList
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from carts.forms import Product_Add_Form


@login_required
def add_to_wish_list(request, product_id):
    product = Product.objects.get(id=product_id)
    if not WishList.objects.filter(user=request.user, product=product):
        wish = WishList()
        wish.user = request.user
        wish.product = product
        wish.save()
    else:
        messages.warning(request, 'You can\'t add the same product!')
    return render(request, 'wish/add_to_wish.html', {'product': product})


@login_required
def wish_list(request):
    user_wish_list = request.user.wish_list.all()
    item_list = []
    form = Product_Add_Form
    for wish in user_wish_list:
        item_list.append(wish.product)
    return render(request, 'wish/wish_list.html', {'wish_list': item_list, 'form': form})


def delete_wish(request, product_id):
    product = Product.objects.get(id=product_id)
    wish = WishList.objects.get(user=request.user, product=product)
    wish.delete()
    redirect('wish:wish_list')
