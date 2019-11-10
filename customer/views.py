import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import F
from django.views import generic

from barber.models import Schedule, BarberShop
from customer.models import Reservation
from BeCute.misc import parse_date

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

        reservation = Reservation(start=start, duration=duration, state='R')
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


class CustomerProfileView(generic.TemplateView):
    template_name = 'customer/profile.html'

    def get_context_data(self, **kwargs):
        context = super(CustomerProfileView, self).get_context_data(**kwargs)
        # TODO filter by user
        user_reservations = Reservation.objects.filter()
        upcoming_reservations = user_reservations.filter(
            state=Reservation.STATE_RESERVED
        ).order_by(
            'start'
        )[:3]
        previous_reservations = user_reservations.filter(
            start__lt=datetime.datetime.now()
        ).order_by('state', '-start')
        context.update(upcoming_reservations=upcoming_reservations, previous_reservations=previous_reservations)
        return context
