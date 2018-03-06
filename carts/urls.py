from django.conf.urls import url
from . import views

app_name = 'carts'

urlpatterns = [
    url(r'^$', views.cart_detail, name='cart_detail'),
    url(r'^add/(?P<product_id>\d+)/$', views.add_to_cart, name='add'),
    url(r'^remove/(?P<product_id>\d+)/$', views.remove_form_cart, name='remove'),

]