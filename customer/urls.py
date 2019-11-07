from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main),
    path('reserve',views.reserve),
    path('search',views.search),
    path('search',views.reserve),
    path('profile',views.profile()),

]
