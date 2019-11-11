import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import F
from django.views import generic

from barber.models import Schedule, BarberShop
from customer.models import Reservation
from BeCute.misc import parse_date, parse_datetime


# from django.contrib.gis.geos.point import Point
# from django.contrib.gis.db.models.functions import Distance


def main(request):
    print("customer index")
    return render(request, 'customer/index.html', context={})


def reserve(request):
    if request.method == 'POST':
        start = parse_datetime(request.POST.get('start', ''))
        try:
            shop = BarberShop.objects.get(id=int(request.POST.get('shop_id')))
            duration = datetime.timedelta(minutes=int(request.POST.get('duration')))
        except (TypeError, ValueError, BarberShop.DoesNotExist):
            shop = None
            duration = None
        if not (start and duration and shop):
            return HttpResponse('bad request')

        if Reservation.objects.filter(
                shop=shop,
                start__lt=start + duration,
                start__gte=start-F('duration')
        ).exists() or not Schedule.objects.filter(
            shop=shop,
            start__lte=start,
            start__gte=start+duration-F('duration')
        ).exists():
            return HttpResponse("requested time is not available")

        Reservation.objects.create(start=start, duration=duration, state='R', shop=shop)
        # todo return result
        return redirect('/customers/profile/')

    else:
        shops = BarberShop.objects.values_list('id', 'name')
        return render(
            request,
            'customer/new_reservation.html',
            {'shops': shops}
        )


def cancel(request, reserve_id):
    if request.method == "POST":
        try:
            Reservation.objects.filter(id=reserve_id).delete()
        except ObjectDoesNotExist:
            pass

        return redirect("/customers/profile")


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
