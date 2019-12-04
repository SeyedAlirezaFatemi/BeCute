from django.db import models

from account.models import CustomUser


# from django.contrib.gis.db import models as spatial_models


class Service(models.Model):
    name = models.CharField(max_length=50)
    duration = models.DurationField()
    price = models.DecimalField(max_digits=6, decimal_places=2)


class BarberShop(models.Model):
    name = models.CharField(max_length=50)
    barber = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=123456)
    introduction = models.CharField(max_length=1000, default="")
    service = models.ManyToManyField(
        Service, through="BarberService", through_fields=("shop", "service")
    )
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    foundation_year = models.IntegerField(max_length=4)

    # TODO: get input fields in signup form

    # location = spatial_models.PointField()


class BarberService(models.Model):
    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)


class Schedule(models.Model):
    shop = models.ForeignKey(BarberShop, on_delete=models.CASCADE)
    start = models.DateTimeField()
    duration = models.DurationField()
