import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect

from barber.models import Schedule, BarberShop
from customer.models import Reservation


# from django.contrib.gis.geos.point import Point
# from django.contrib.gis.db.models.functions import Distance


def main(request):
    print("customer index")
    return render(request, 'customer/index.html', context={})


def reserve(request, shop_uid, start=None, end=None):
    if request.method == 'POST':

        day = int(request.POST.get('day', False))
        year = int(request.POST.get('year', False))
        hour = int(request.POST.get('hour', False))
        month = int(request.POST.get('month', False))
        minute = int(request.POST.get('minute', False))

        # todo check if time is available

        reservation = Reservation(
            start=datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute),
            duration=datetime.timedelta(
                minutes=int(request.POST.get('duration', False))
            ),
            state='R',
        )
        reservation.save()

        # todo return result
        return redirect('/customer/')

    elif request.method == 'GET' and start is not None and end is not None:

        end = parse_date(end)
        start = parse_date(start)

        try:
            shop = BarberShop.objects.get(id=shop_uid)
            schedules = Schedule.objects.filter(shop=shop_uid, start__lt=end, start__gt=start).all()
            reserves = Reservation.objects.filter(shop=shop_uid, start__lt=end, start__gt=start).all()

            print(len(schedules), "\t", schedules)
            return render(request, 'customer/reserve.html',
                          {'shop': shop, 'reserves': reserves, 'schedules': schedules})

        except ObjectDoesNotExist:
            pass

    return HttpResponse(" this is reserve page of costumer")


def cancel(request, start, end):
    if request.method == "POST":

        try:
            reserve_id = int(request.POST.get('reserve_id'))
            Reservation.objects.filter(id=reserve_id).delete()
        except ObjectDoesNotExist:
            pass

        return redirect("/customer/cancel/%s/%s" % (start, end))

    else:
        # fixme filter for current user
        reserves = Reservation.objects.filter(start__lt=parse_date(end), start__gt=parse_date(start)).all()
        return render(request, 'customer/cancel.html', {'reserves': reserves})


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


def parse_date(date_str):
    date_str = list(map(int, date_str.split("-")))
    return datetime.datetime(year=date_str[0], month=date_str[1], day=date_str[2])
