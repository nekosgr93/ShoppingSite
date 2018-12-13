from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from paypal.standard.forms import PayPalPaymentsForm

from .forms import User_address_choice_form, New_shipping_address_form
from .models import Order
from carts.cart import Auth_User_Cart
from accounts.models import UserAddress
from ShoppingSite.settings import PAYPAL_REVEIVER_EMAIL


@login_required
def choose_shipping(request):
    use_shipping_form = User_address_choice_form()
    new_shipping_address_form = New_shipping_address_form()
    use_address = UserAddress.objects.filter(user=request.user)
    if request.method == 'POST':
        if 'use' in request.POST:
            # If the order use the default address
            use_shipping_form = User_address_choice_form(request.POST)
            if use_shipping_form.is_valid():
                request.session['address'] = use_shipping_form.cleaned_data

        elif 'save' in request.POST:
            # If the order add a new address
            new_shipping_address_form = New_shipping_address_form(request.POST)
            if new_shipping_address_form.is_valid():
                request.session['address'] = new_shipping_address_form.cleaned_data
        return redirect("orders:checkout")
    return render(request, "orders/shipping.html", {'user_address': use_address,
                                                    'use_shipping_form': use_shipping_form,
                                                    'new_shipping_address_form': new_shipping_address_form})


class Found_address(object):
    def __init__(self, request):
        if 'address_id' in request.session.get('address'):
            address_id = request.session.get('address')['address_id']
            address = UserAddress.objects.get(id=address_id)
            self.full_name = address.full_name
            self.postal_code = address.postal_code
            self.country = address.country
            self.address1 = address.address1
            self.address2 = address.address2
            self.phone_number = address.phone_number

        else:
            address = request.session.get('address')
            self.full_name = address['shipping_full_name']
            self.postal_code = address['shipping_postal_code']
            self.country = address['shipping_country']
            self.address1 = address['shipping_address1']
            self.address2 = address['shipping_address2']
            self.phone_number = address['shipping_phone_number']


@login_required
def checkout(request):
    checkout_address = Found_address(request)
    cart = Auth_User_Cart(request)
    if request.method == "POST":
        order = Order(
            user=request.user,
            cart=cart.cart,
            shipping_full_name=checkout_address.full_name,
            shipping_postal_code=checkout_address.postal_code,
            shipping_country=checkout_address.country,
            shipping_address1=checkout_address.address1,
            shipping_address2=checkout_address.address2,
            shipping_phone_number=checkout_address.phone_number
        )
        order.save()
        request.session['order_id'] = order.id
        cart.checked_out_cart()
        del request.session['address']
        return redirect("orders:payment")
    return render(request, 'orders/checkout.html', {'cart': cart, 'checkout_address': checkout_address})


@login_required
def paypal_payment(request):
    order_id = request.session['order_id']
    order = Order.objects.get(id=order_id)
    host = request.get_host()
    paypal_dict = {
        'business': PAYPAL_REVEIVER_EMAIL,
        'amount': order.cart.total,
        'item_name': order.cart.id,
        'invoice': order_id,
        'notify_url': 'http://{}{}'.format(host, reverse('paypal-ipn')),
        'return_url': 'http://{}{}'.format(host, reverse('orders:finish_order')),
        'cancel_return': 'http://{}{}'.format(host, reverse('orders:order_list')),
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    del request.session['order_id']
    return render(request, 'orders/payment.html', {'form': form})


class Finish_Page(TemplateView):
    template_name = 'orders/finish_page.html'


class OrderList(LoginRequiredMixin, ListView):
    context_object_name = 'order_list'
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
