"""BeCute URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from BeCute.views import logout_view, index_view, error_view
from django.contrib.auth.decorators import login_required
from haystack.views import basic_search
from . import views

urlpatterns = [
    path('', index_view, name='index'),
    path("admin/", admin.site.urls),
    path("customers/", include("customer.urls")),
    path("barbers/", include("barber.urls")),
    path("accounts/", include("account.urls")),
    path(r'logout/', logout_view, name='logout'),
    path(r'search/', login_required(basic_search), name='basic_search'),
    path("error/", error_view, name="error")
]
