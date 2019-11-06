from django.db import models


class Reservation(models.Model):
    STATES = (
        ('R', 'reserved'),
        ('D', 'done'),
        ('C', 'canceled'),
    )

    # barber = models.ForeignKey(USER, on_delete=models.CASCADE) TODO link to barber
    # customer = models.ForeignKey(USER, on_delete=models.CASCADE) TODO link to user
    start = models.DateTimeField()
    duration = models.DurationField()
    state = models.CharField(max_length=1, choices=STATES)
