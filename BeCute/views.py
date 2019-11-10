from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth.forms import UserCreationForm

from account.models import CustomUser
from barber.models import BarberShop


def landing(request):
    return render(request, 'index.html', context={})

