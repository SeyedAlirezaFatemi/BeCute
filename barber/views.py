import datetime

from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist


from BeCute.misc import parse_date
from customer.models import Reservation
from barber.models import Schedule, BarberShop
from account.models import CustomUser


def main(request):
    return render(request, 'barber/index.html', context={})


def profile(request):
    return HttpResponse(" this is profile page of costumer")


def schedule(request, start=None, end=None):
    # fixme: replace 1 by shop_id from shop retrieved by barber user_id(fixed)
    current_barber = CustomUser.objects.filter(username=request.user.username).all()[0]
    shop = BarberShop.objects.filter(barber=current_barber).all()[0]
    if request.method == "POST":
        if request.POST.get('type') == "add":

            day = int(request.POST.get('day', False))
            year = int(request.POST.get('year', False))
            hour = int(request.POST.get('hour', False))
            month = int(request.POST.get('month', False))
            minute = int(request.POST.get('minute', False))
            start_dt = datetime.datetime(year=year, month=month, day=day, hour=hour, minute=minute)
            duration = datetime.timedelta(
                minutes=int(request.POST.get('duration', False))
            )

            if Schedule.objects.filter(
                    Q(start__lte=start_dt, start__gt=start_dt-F('duration')) |
                    Q(start__lt=start_dt+duration, start__gte=start_dt-F('duration')) |
                    Q(start__gte=start_dt, start__lte=start_dt+duration-F('duration')),
                    shop=shop,
            ).exists():
                return HttpResponse("there is an overlap with other free times")

            free_time = Schedule(shop=shop, start=start_dt, duration=duration)
            free_time.save()

        else:
            # todo don't let barber cancel times with reservations(fixed)
            try:
                if Reservation.objects.filter(shop=shop,state='R'):
                    return HttpResponse("this time is reserved by a customer!")
                Schedule.objects.filter(id=int(request.POST.get('free_time'))).delete()
            except ObjectDoesNotExist:
                pass

        return redirect('/barber/schedule/%s/%s/' % (start, end))

    else:
        reservations = Reservation.objects.filter(shop=shop, start__gte=parse_date(start),
                                                  start__lte=parse_date(end)).all()
        schedules = Schedule.objects.filter(shop=shop, start__gte=parse_date(start), start__lte=parse_date(end)).all()
        return render(request, 'barber/schedule.html',
                      {'schedules': schedules, 'reservations': reservations, 'start_time': start, 'end_time': end}
                      )
