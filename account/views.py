from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.views import generic

from BeCute.misc import get_login_redirect_url, get_signup_redirect_url
from account.forms import SignupForm


def landing(request):
    return render(request, "index.html", context={})  # todo create barber index


class Signup(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = SignupForm

    def get(self, request, *args, **kwargs):
        try:
            if request.user:
                if request.user.type == 'barber':
                    return redirect("barber-profile")
                return redirect("customer-profile")
        except:
            return super().get(self, request, *args, **kwargs)

    def get_success_url(self):
        return get_signup_redirect_url()

    def post(self, request, *args, **kwargs):
        resp = super(Signup, self).post(request, *args, **kwargs)
        # user = self.object
        # if user:
        #     login(request, user)
        return resp


class Login(LoginView):
    def get_success_url(self):
        return get_login_redirect_url(self.request.user)


def profile(request):
    return render(request, "base/base_profile.html", context={"user": request.user})
