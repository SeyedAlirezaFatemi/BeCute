from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path('', views.main),

    path('search/', login_required(views.search)),
    path('profile/', login_required(views.CustomerProfileView.as_view()), name='customer-profile'),

    path('reserve/<int:shop_uid>/', login_required(views.reserve)),
    path('reserve/<int:shop_uid>/<str:start>/<str:end>/', login_required(views.reserve)),

    path('cancel/<str:start>/<str:end>/', login_required(views.cancel)),

]
