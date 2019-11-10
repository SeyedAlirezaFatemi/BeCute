import datetime

from django.urls import reverse_lazy

from customer.models import CustomUser


def parse_date(date_str):
    date_str = list(map(int, date_str.split("-")))
    return datetime.datetime(year=date_str[0], month=date_str[1], day=date_str[2])


def get_login_redirect_url(user):
    if user.type == CustomUser.USER_TYPE_BARBER:
        return reverse_lazy('barber-profile')
    elif user.type == CustomUser.USER_TYPE_CLIENT:
        return reverse_lazy('customer-profile')
    return reverse_lazy('profile')
