from django.contrib.auth.decorators import login_required
from django.urls import path

from . import views

urlpatterns = [
    path("", views.main),
    path("search/", login_required(views.search)),
    path(
        "profile/",
        login_required(views.CustomerProfileView.as_view()),
        name="customer-profile",
    ),
    path("reserve/", login_required(views.reserve), name="reserve"),
    path("cancel/<int:reserve_id>/", login_required(views.cancel), name="cancel"),
    path(
        "<str:barbershop_name>/comment/",
        login_required(views.CreateComment.as_view()),
        name="comment",
    ),
    path("<str:customer_username>/profile",
        views.profile,
         name='info')
]
