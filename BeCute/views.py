from django.contrib.auth import logout
from django.shortcuts import render


def index_view(request):
    return render(request, "index.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "registration/login.html")
