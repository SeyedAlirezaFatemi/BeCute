from django.db import models

from barber.models import BarberShop

from django.contrib.auth.models import AbstractUser, User


class Reservation(models.Model):
    STATE_RESERVED = 'R'
    STATE_DONE = 'D'
    STATE_CANCELED = 'C'
    STATES = (
        (STATE_RESERVED, 'reserved'),
        (STATE_DONE, 'done'),
        (STATE_CANCELED, 'canceled'),
    )

    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, default=1)
    # customer = models.ForeignKey(USER, on_delete=models.CASCADE) TODO link to user
    start = models.DateTimeField()
    duration = models.DurationField()
    state = models.CharField(max_length=1, choices=STATES)


class CustomUser(AbstractUser):
    USER_TYPE_CLIENT = 'client'
    USER_TYPE_BARBER = 'barber'
    USER_TYPES = ((USER_TYPE_CLIENT, 'client'), (USER_TYPE_BARBER, 'barber'))
    type = models.CharField(max_length=100, choices=USER_TYPES)
