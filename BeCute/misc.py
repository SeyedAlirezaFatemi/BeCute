import datetime

from django.urls import reverse_lazy

from customer.models import CustomUser


def parse_date(date_str: str):
    try:
        return datetime.datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def parse_datetime(datetime_str: str):
    try:
        return datetime.datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        return None


def get_login_redirect_url(user):
    if user.type == CustomUser.USER_TYPE_BARBER:
        return reverse_lazy("barber-profile")
    elif user.type == CustomUser.USER_TYPE_CLIENT:
        return reverse_lazy("customer-profile")
    return reverse_lazy("profile")


def get_signup_redirect_url():
    return reverse_lazy("login")
