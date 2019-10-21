from django.http import HttpResponse
from django.shortcuts import render


def main(request):
    return render(request, 'customer/index.html', context={})
