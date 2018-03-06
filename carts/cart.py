from .models import Cart, CartItem
from django.contrib.auth.models import User
from django.shortcuts import Http404
from django.core.exceptions import MultipleObjectsReturned
from decimal import Decimal
from products.models import Product
from django.contrib import messages

class Anon_User_Cart(object):
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def save(self):
        self.session['cart'] = self.cart
        self.session.modified = True

    def add(self, product, quantity):
        product_id = str(product.id)
        product = Product.objects.get(id=product_id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': quantity,
                                     'price': str(product.price),
                                     }

        else:
            self.add_to_update(product, quantity)
        self.save()

    def add_to_update(self, product, quantity):
        product_id = str(product.id)
        self.cart[product_id]['quantity'] += quantity

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_cart_item(self):
        product_id = self.cart.keys()
        products = Product.objects.filter(id__in=product_id)
        for product in products:
            self.cart[str(product.id)]['product'] = product
        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['subtotal'] = (item['price']*item['quantity'])
            yield item

    def get_total_price(self):
        return sum(item['subtotal'] for item in self.cart.values())

    def clear(self):
        del self.session['cart']
        self.session.modified = True


class Auth_User_Cart(object):
    def __init__(self, request):
        try:
            self.cart = Cart.objects.get(user=request.user, activate=True)
            self.combine_the_anon_cart(request)
        except Cart.DoesNotExist:
            self.cart = Cart()
            self.cart.user = request.user
            self.cart.save()
            self.combine_the_anon_cart(request)
            self.get_cart_item = self.get_cart_item()

    def add(self, product, quantity):
        exist_check = CartItem.objects.filter(product=product)
        if not exist_check:
            if product.user != self.cart.user:
                item = CartItem()
                item.cart = self.cart
                item.product = product
                item.price = product.price
                item.quantity = quantity
                item.save()
                self.cart.calculate_total()
        else:
            self.add_to_update(product, quantity)

    def add_to_update(self, product, quantity):
        item = CartItem.objects.get(cart=self.cart, product=product)
        item.quantity += quantity
        item.save()
        self.cart.calculate_total()

    def combine_the_anon_cart(self, request):
        """combine the anon user cart and
        delete it after the user login"""
        cart = request.session.get('cart')
        if cart:
            for item in cart.items():
                product = Product.objects.get(id=item[0])
                if product.user == request.user:
                    messages.error(request, 'You can\'t buy your product')
                else:
                    quantity = item[1]['quantity']
                    self.add(product, quantity)
            del request.session['cart']

    def update(self, product, quantity):
        item = CartItem.objects.get(cart=self.cart, product=product)
        item.quantity = quantity
        item.subtotal = item.price*item.quantity
        item.save()
        self.cart.calculate_total()

    def remove(self, product):
        item = CartItem.objects.get(cart=self.cart, product=product)
        if item:
            item.delete()
        self.cart.calculate_total()

    def get_cart_item(self):
        return self.cart.get_cart_items()

    def get_total_price(self):
        return self.cart.total

    def checked_out_cart(self):
        """if the cart has checked out ,
           set it to inactivate"""
        self.cart.activate = False
        self.cart.save()













# def create_anon_user_cart(request):
#     anon_cart_id = request.session.session_key
#     cart = Cart(session=anon_cart_id)
#     cart.save()
#     request.session['anon_cart_id'] = anon_cart_id
#     request.session['carry_over_cart'] = True
#     return cart


# def retrieve_anon_user_cart(request):
#     anon_cart_id = request.session.get('anon_cart_id')
#     cart = Cart.objects.get(session=anon_cart_id)
#     return cart


# def assign_anon_cart_to_user(request):
#     try:
#         anon_cart_id = request.session.get('anon_cart_id')
#         cart = Cart.objects.get(session=anon_cart_id)
#         if cart.user is None and request.user.is_authenticated() and request.session.get('carry_over_cart'):
#             user = User.objects.get(username=request.user)
#             cart.user = user
#             del request.session['anon_cart_id']
#             del request.session['carry_over_cart']
#             cart.save()
#     except KeyError:
#         raise Http404
#     return cart
#
#
# def create_auth_user_cart(request):
#     cart = Cart(session=request.session.session_key)
#     user = User.objects.get(username=request.user)
#     cart.user = user
#     cart.save()
#     return cart
#
#
# def retrieve_auth_user_cart(request):
#     cart = Cart.objects.get(user=request.user)
#     return cart
#
#
# def create_or_retrieve_cart(request):
#     if request.user.is_authenticated():
#         try:
#             cart = retrieve_auth_user_cart(request)
#         except Cart.DoesNotExist:
#             cart = create_auth_user_cart(request)
#         except MultipleObjectsReturned:
#             cart = create_combined_cart(request)
#
#     else:
#         try:
#             cart = retrieve_anon_user_cart(request)
#         except Cart.DoesNotExist:
#             cart = create_anon_user_cart(request)
#     return cart
#
# def create_combined_cart(request):
#     cart_list = Cart.objects.filter(username=request.user)
#     for cart in cart_list:
#         cart.activate = False
#         cart.save()
#     new_cart = create_auth_user_cart(request)
#     for cart in cart_list:
#         for item in cart.get_cart_items():
#             item.cart = new_cart
#             item.save()
#     new_cart.save()
#     return new_cart

