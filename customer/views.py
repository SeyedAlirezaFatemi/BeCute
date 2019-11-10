import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import F

from barber.models import Schedule, BarberShop
from customer.models import Reservation
from BeCute.misc import parse_date
from account.models import CustomUser

# from django.contrib.gis.geos.point import Point
# from django.contrib.gis.db.models.functions import Distance


def main(request):
    print("customer index")
    return render(request, 'customer/index.html', context={})


def reserve(request, shop_uid, start=None, end=None):
    current_user = CustomUser.objects.filter(username=request.user.username).all()[0]
    if request.method == 'POST':
        barber = BarberShop.objects.get(id=shop_uid)

        day = int(request.POST.get('day', False))
        year = int(request.POST.get('year', False))
        hour = int(request.POST.get('hour', False))
        month = int(request.POST.get('month', False))
        minute = int(request.POST.get('minute', False))
        start = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
        duration = datetime.timedelta(
            minutes=int(request.POST.get('duration', False))
        )

        if Reservation.objects.filter(
                shop=shop_uid,
                start__lt=start + duration,
                start__gte=start-F('duration')
        ).exists() or not Schedule.objects.filter(
            shop=shop_uid,
            start__lte=start,
            start__gte=start+duration-F('duration')
        ).exists():
            return HttpResponse("requested time is not available")

        print("=========================================================================")
        print(current_user)
        print(CustomUser.objects.all())
        print("=========================================================================")

        reservation = Reservation(shop=barber, customer=current_user, duration=duration, start=start, state='R')
        reservation.save()

        # todo return result
        return HttpResponse('your reserve is registered')

    elif request.method == 'GET' and start is not None and end is not None:

        end = parse_date(end)
        start = parse_date(start)

        try:
            shop = BarberShop.objects.get(id=shop_uid)
            schedules = Schedule.objects.filter(shop=shop_uid, start__lte=end, start__gte=start).all()
            reserves = Reservation.objects.filter(shop=shop_uid, start__lte=end, start__gte=start).all()

            print(len(schedules), "\t", schedules)
            return render(request, 'customer/reserve.html',
                          {'shop': shop, 'reserves': reserves, 'schedules': schedules})

        except ObjectDoesNotExist:
            pass


def cancel(request, start, end):
    current_user = CustomUser.objects.get(username=request.user.username)
    if request.method == "POST":

        try:
            reserve_id = int(request.POST.get('reserve_id'))
            Reservation.objects.filter(id=reserve_id).delete()
        except ObjectDoesNotExist:
            pass

        return redirect("/customer/cancel/%s/%s" % (start, end))

    else:
        # fixme filter for current user
        reserves = Reservation.objects.filter(customer=current_user, start__lt=parse_date(end), start__gt=parse_date(start)).all()
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
