from django.db import models
from barber.models import BarberShop


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
