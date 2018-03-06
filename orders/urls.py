from django.conf.urls import url
from . import views

app_name = 'orders'

urlpatterns = [
    url(r'^$', views.order_list, name='order_list'),
    url(r'^order_detail/(?P<pk>\d+)/$', views.order_detail, name='order_detail'),
    url(r'^shipping/$', views.choose_shipping, name='shipping'),
    url(r'^payment/$', views.choose_payment, name='payment'),
    url(r'^checkout/$', views.checkout, name='checkout'),
    url(r'finished/$', views.Finish_Page.as_view(), name='finish_order'),

]