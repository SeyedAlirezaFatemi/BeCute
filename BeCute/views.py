from django.contrib.auth import logout
from django.shortcuts import render
from haystack.generic_views import SearchView


def index_view(request):
    return render(request, "index.html")


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return render(request, "registration/login.html")

def error_view(request):
    request.session['page'] = 'profile'
    return render(request, "../templates/error/error.html")
