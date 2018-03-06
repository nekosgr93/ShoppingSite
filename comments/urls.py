from django.conf.urls import url
from . import views

app_name = 'comments'

urlpatterns = [
    url(r'^new/(?P<product_id>\d+)/$', views.comment, name='new_comment'),
    url(r'^edit/(?P<id>\d+)/$', views.edit_comment, name='edit'),
    url(r'^remove/(?P<id>\d+)/$', views.remove_comment_confirm, name='remove'),

]