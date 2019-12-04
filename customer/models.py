from django.db import models

from barber.models import BarberShop
from account.models import CustomUser


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
    state = models.CharField(max_length=1, choices=STATES)
