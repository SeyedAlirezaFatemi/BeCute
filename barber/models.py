from django.db import models
from django.urls import reverse

from account.models import CustomUser


# from django.contrib.gis.db import models as spatial_models


class Service(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)


class BarberShop(models.Model):
    name = models.CharField(max_length=50)
    barber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=123456)
    introduction = models.CharField(max_length=1000, default="")
    service = models.ManyToManyField(
        Service, through="BarberService", through_fields=("shop", "service")
    )
    address = models.CharField(max_length=200, default="")
    city = models.CharField(max_length=50, default="")
    foundation_year = models.CharField(max_length=4, default="2019")
    phone = models.CharField(max_length=20, default="")

    # location = spatial_models.PointField()

    def get_absolute_url(self):
        return reverse('barber_info', kwargs={'barbershop_id': self.name})


class BarberService(models.Model):
    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Schedule(models.Model):
    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.DurationField()
