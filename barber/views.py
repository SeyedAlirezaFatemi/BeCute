from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return render(request, 'barber/index.html', context={})


def profile(request):
    return HttpResponse(" this is profile page of costumer")


def schedule(request):
    return HttpResponse(" this is schedule page of costumer")