from django.conf.urls import url
from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.OrderList.as_view(), name='order_list'),
    url(r'^shipping/$', views.choose_shipping, name='shipping'),
    url(r'^payment/$', views.paypal_payment, name='payment'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'finished/$', views.Finish_Page.as_view(), name='finish_order'),
]
