from django.http import HttpResponse
from django.shortcuts import render
import json
from barber.models import BarberShop
from django.contrib.gis.geos.point import Point
from django.contrib.gis.db.models.functions import Distance

def main(request):
    return render(request, 'customer/index.html', context={})


def reserve(request):
    return HttpResponse(" this is search page of costumer")


def search(request):
    if request.method == 'GET':
        body = json.loads(request.body)
        point = Point(body["long"], body["latt"])

        search_result = BarberShop.objects.annotate(
            distance=Distance('location', point)
        ).order_by('distance').all()

        return HttpResponse(json.dumps(search_result))

    return HttpResponse(" this is reserve page of costumer")


def profile(request):
    return HttpResponse(" this is profile page of costumer")