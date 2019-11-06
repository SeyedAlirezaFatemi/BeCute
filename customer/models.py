from django.db import models


class Service(models.Model):
    name = models.CharField(max_length="50")
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)


class BarberShop(models.Model):
    # barber = models.ForeignKey(USER, on_delete=models.CASCADE) TODO link to barber
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
