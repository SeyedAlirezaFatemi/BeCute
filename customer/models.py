from django.db import models

from account.models import CustomUser
from barber.models import BarberShop, Service


class Reservation(models.Model):
    STATE_RESERVED = "R"
    STATE_DONE = "D"
    STATE_CANCELED = "C"
    STATES = (
        (STATE_RESERVED, "reserved"),
        (STATE_DONE, "done"),
        (STATE_CANCELED, "canceled"),
    )

    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE, default=1234567)
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1234567)
    start = models.DateTimeField()
    duration = models.DurationField()
    service = models.ForeignKey(Service, on_delete=models.CASCADE, default='')
    state = models.CharField(max_length=1, choices=STATES)


class Comment(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    barbershop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    rate = models.IntegerField(default=0, name='rate')
    content = models.CharField(max_length=1000, default='Nice!')
