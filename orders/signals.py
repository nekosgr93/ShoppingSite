from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received

from .models import Order


def confirm_payment(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        print('recieve Payment')
        if ipn_obj.receiver_email != 'zerofoxy05-facilitator@gmail.com':
            return
        order_id = ipn_obj.invoice
        order = Order.objects.get(id=order_id)
        order.paid = True
        order.save()


valid_ipn_received.connect(confirm_payment)
