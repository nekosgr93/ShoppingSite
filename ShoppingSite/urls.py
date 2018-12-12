"""ShoppingSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^query/$', views.product_query, name='query'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    url(r'^welcome/', views.Welcome.as_view(), name='welcome'),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^carts/', include('carts.urls', namespace='carts')),
    url(r'^orders/', include('orders.urls', namespace='orders')),
    url(r'^comments/', include('comments.urls', namespace='comments')),
    url(r'^wish/', include('wish.urls', namespace='wish')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
