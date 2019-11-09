from django.db import models

from barber.models import BarberShop

from django.contrib.auth.models import AbstractUser, User



class Reservation(models.Model):
    STATES = (
        ('R', 'reserved'),
        ('D', 'done'),
        ('C', 'canceled'),
    )

    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, default=1)
    # customer = models.ForeignKey(USER, on_delete=models.CASCADE) TODO link to user
    start = models.DateTimeField()
    duration = models.DurationField()
    state = models.CharField(max_length=1, choices=STATES)

class CustomUser(AbstractUser):
    type = models.CharField(max_length=100, choices=(('client', 'client'), ('barber', 'barber')))


