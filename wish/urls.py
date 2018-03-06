from django.conf.urls import url
from . import views

app_name = 'wish'

urlpatterns = [
    url(r'^add/(?P<product_id>\d+)/$', views.add_to_wish_list, name='add'),
    url(r'^list/$', views.wish_list, name='wish_list'),
    url(r'^delete/(?P<product_id>\d+)/$', views.delete_wish, name='delete')
]
