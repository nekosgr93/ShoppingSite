from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView

from .forms import User_address_choice_form, New_shipping_address_form
from .models import Order
from .order import Found_address
from carts.cart import Auth_User_Cart
from accounts.models import UserAddress


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
        return redirect("orders:payment")
    return render(request, "orders/shipping.html", {'user_address': use_address,
                                                    'use_shipping_form': use_shipping_form,
                                                    'new_shipping_address_form': new_shipping_address_form})


@login_required
def choose_payment(request):
    if request.method == 'POST':
        return redirect("orders:checkout")
    return render(request, "orders/payment.html")


def found_address(request):
    if 'address_id' in request.session.get('address'):
        address_id = request.session.get('address')['address_id']
        address = UserAddress.objects.get(id=address_id)
    else:
        address = request.session.get('address')
    return address


@login_required
def checkout(request):
    checkout_address = Found_address(request)
    cart = Auth_User_Cart(request)
    if request.method == "POST":
        order = Order()
        order.user = request.user
        order.cart = cart.cart
        if 'address_id' in request.session.get('address'):
            address_id = request.session.get('address')['address_id']
            address = UserAddress.objects.get(id=address_id)
            order.address = address
            order.paid = True
            order.save()
            order.cart.paid_cart()
        else:
            cd = request.session.get('address')
            order.shipping_full_name = cd['shipping_full_name']
            order.shipping_postal_code = cd['shipping_postal_code']
            order.shipping_country = cd['shipping_country']
            order.shipping_address = cd['shipping_address']
            order.shipping_phone_number = cd['shipping_phone_number']
            order.paid = True
            order.save()
            order.cart.paid_cart()
            del request.session['address']

        return redirect("orders:finish_order")
    return render(request, 'orders/checkout.html', {'cart': cart, 'checkout_address': checkout_address})


class OrderList(LoginRequiredMixin, ListView):
    context_object_name = 'order_list'
    template_name = 'orders/order_list.html'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderDetail(LoginRequiredMixin, DetailView):
    context_object_name = 'order'
    template_name = 'orders/order_detail.html'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return Order.objects.get(user=self.request.user, pk=pk)


class Finish_Page(TemplateView):
    template_name = 'orders/finish_page.html'
