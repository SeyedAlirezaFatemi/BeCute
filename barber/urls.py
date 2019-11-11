from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

urlpatterns = [
    path('', login_required(views.main) , name='main'),
    path('profile/', login_required(views.BarberProfileView.as_view()), name='barber-profile'),

    path('schedule/', login_required(views.schedule), name='schedule'),
]
