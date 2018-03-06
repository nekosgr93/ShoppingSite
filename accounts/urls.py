from django.conf.urls import url
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'accounts'

urlpatterns = [
    url(r'^login/', LoginView.as_view(template_name="accounts/login.html"), name='login'),
    url(r'^logout/', LogoutView.as_view(), name='logout'),
    url(r'^signup/', views.SignupView, name='signup'),
    url(r'^profiles/(?P<username>[-\w]+)/$', views.User_profile, name='profiles'),
    url(r'^profiles/(?P<username>[-\w]+)/edit/$', views.edit_profile, name='profile_edit'),
    url(r'^address/(?P<username>[-\w]+)/$', views.AddressList.as_view(), name='user_address'),
    url(r'^address/(?P<username>[-\w]+)/new/$', views.create_address, name='create_address'),
    url(r'^address/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.UpdateAddress.as_view(), name="update_address"),
    url(r'delete/(?P<username>[-\w]+)/(?P<pk>\d+)/$', views.DeleteAddress.as_view(), name="delete_address")
]