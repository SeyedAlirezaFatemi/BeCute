from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.main , name='main'),
    path('profile/', views.profile, name='profile'),

    path('schedule/', views.schedule, name='schedule'),
    path('schedule/<str:start>/<str:end>/', views.schedule, name='schedule')
]
