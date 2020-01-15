from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", login_required(views.main), name="main"),
    path(
        "profile/",
        login_required(views.BarberProfileView.as_view()),
        name="barber-profile",
    ),
    path("schedule/", login_required(views.schedule), name="schedule"),
    path(
        "cancel-schedule/<int:schedule_id>/",
        login_required(views.cancel_schedule),
        name="cancel-schedule",
    ),
    path('<str:barbershop_id>/profile',
         views.profile,
         name='barber_info'),
    path('add-service/', login_required(views.add_service), name='add_service'),
    path('edit-serivce/', login_required(views.edit_service), name='edit_service'),
]
