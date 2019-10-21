from django.http import HttpResponse
from django.shortcuts import render


def landing(request):
    return render(request, 'index.html', context={})


def signup(request):
    return HttpResponse('signup page')


def login(request):
    return HttpResponse('login page')
