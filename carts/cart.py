from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist

from .models import Cart, CartItem
from products.models import Product


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
            self.cart[product_id] = {
                'quantity': quantity,
                'price': str(product.price)
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
        except ObjectDoesNotExist:
            self.cart = Cart()
            self.cart.user = request.user
            self.cart.save()
            self.combine_the_anon_cart(request)
            self.get_cart_item = self.get_cart_item()

    def add_or_update(self, product, quantity):
        try:
            item = CartItem.objects.get(cart=self.cart, product=product)
        except ObjectDoesNotExist:
            item = CartItem(
                cart=self.cart,
                product=product,
                price=product.price,
                quantity=quantity
            )
            item.save()
        else:
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
