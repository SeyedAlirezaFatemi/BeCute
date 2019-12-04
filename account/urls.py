from django.contrib.auth.decorators import login_required
from django.urls import path, include
from . import views

urlpatterns = [
    path("signup/", views.Signup.as_view(), name="signup"),
    path("login/", views.Login.as_view(), name="login"),
    path("profile/", login_required(views.profile), name="profile"),
    path("", include("django.contrib.auth.urls"), name="authentication"),
]
