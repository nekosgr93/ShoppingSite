from django.conf.urls import url
from . import views

app_name = 'products'

urlpatterns = [
    url(r'^new/$', views.CreateProduct.as_view(), name="create_product"),
    url(r'^(?P<username>[-\w]+)/$', views.ProductList.as_view(), name="product_list"),
    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/$', views.ProductDetail.as_view(), name="product_detail"),
    url(r'^(?P<username>[-\w]+)/(?P<slug>[-\w]+)/edit/$', views.UpdateProduct.as_view(), name="update_product"),
    url(r'^delete/(?P<username>[-\w]+)/(?P<slug>[-\w]+)/$', views.DeleteProduct.as_view(), name="delete_product"),
]
