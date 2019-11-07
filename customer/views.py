from django.http import HttpResponse
from django.shortcuts import render
import json
import datetime
from customer.models import Reservation
from barber.models import BarberShop
# from django.contrib.gis.geos.point import Point
# from django.contrib.gis.db.models.functions import Distance


def main(request):
    print("customer index")
    return render(request, 'customer/index.html', context={})


def reserve(request):#, barber):
    print(123)
    if request.method == 'POST':

        body = json.loads(request.body)

        day = body['day']
        year = body['year']
        hour = body['hour']
        month = body['month']
        minute = body['minute']

        reservation = Reservation(
            start=datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute),
            duration=datetime.timedelta(minutes=int(body['duration'])),
            state='R',
        )
        reservation.save()

        # todo return reult
        return render(request, "customer/index.html")

    elif request.method == 'GET':

        pass

    return HttpResponse(" this is reserve page of costumer")


def search(request):
    # if request.method == 'GET':
    #     body = json.loads(request.body)
    #     point = Point(body["long"], body["latt"])

        # search_result = BarberShop.objects.annotate(
        #     distance=Distance('location', point)
        # ).order_by('distance').all()

        # return HttpResponse(json.dumps(search_result))

    return HttpResponse(" this is search page of costumer")


def profile(request):
    return HttpResponse(" this is profile page of costumer")