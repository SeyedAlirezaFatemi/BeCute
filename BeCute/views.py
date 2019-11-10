from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.views import generic
from django.contrib.auth import login

from BeCute.misc import get_login_redirect_url
from .forms import SignupForm


def landing(request):
    return render(request, 'index.html', context={})


# def signup(request):
#     if request.POST:
#
#         user = CustomUser.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
#         user.first_name = request.POST['first_name']
#         user.last_name = request.POST['last_name']
#         user.type = request.POST['type']
#         user.save()
#         return HttpResponse("signed up successful")
#
#     return render(request, 'registration/signup.html')


class Signup(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = SignupForm

    def get_success_url(self):
        return get_login_redirect_url(self.request.user)

    def post(self, request, *args, **kwargs):
        resp = super(Signup, self).post(request, *args, **kwargs)
        user = self.object
        if user:
            login(request, user)
        return resp


class Login(LoginView):
    def get_success_url(self):
        return get_login_redirect_url(self.request.user)


def profile(request):
    return render(request, 'base/base_profile.html', context={'user': request.user})
