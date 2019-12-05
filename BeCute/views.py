from django.contrib.auth import logout
from django.shortcuts import render


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "registration/login.html")