from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib.auth import login
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
    success_url = reverse_lazy('profile')

    def post(self, request, *args, **kwargs):
        resp = super(Signup, self).post(request, *args, **kwargs)
        user = self.object
        if user:
            login(request, user)
        return resp


def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))

    return HttpResponse(f"you are {request.user.username}")
