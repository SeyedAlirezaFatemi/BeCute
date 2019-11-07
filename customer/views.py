from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return render(request, 'customer/index.html', context={})


def reserve(request):
    return HttpResponse(" this is search page of costumer")


def search(request):
    return HttpResponse(" this is reserve page of costumer")


def profile(request):
    return HttpResponse(" this is profile page of costumer")