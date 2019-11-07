from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main , name='main'),
    path('', views.profile, name='profile'),
    path('', views.schedule, name='schedule')
]
