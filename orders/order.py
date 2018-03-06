from .models import Order
from accounts.models import UserAddress

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
            cd = request.session.get('address')
            self.full_name = cd['shipping_full_name']
            self.postal_code = cd['shipping_postal_code']
            self.country = cd['shipping_country']
            self.address1 = cd['shipping_address1']
            self.address2 = cd['shipping_address2']
            self.phone_number = cd['shipping_phone_number']