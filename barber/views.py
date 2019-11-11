import datetime

from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.views import generic


from BeCute.misc import parse_datetime
from customer.models import Reservation
from barber.models import Schedule, BarberShop


def main(request):
    return render(request, 'barber/index.html', context={})


class BarberProfileView(generic.TemplateView):
    template_name = 'barber/profile.html'

    def get_context_data(self, **kwargs):
        context = super(BarberProfileView, self).get_context_data(**kwargs)

        # TODO fix this so it retrieves shop from the user
        shop = BarberShop.objects.first()

        shop_reservations = Reservation.objects.filter(shop=shop)
        upcoming_reservations = shop_reservations.filter(
            state=Reservation.STATE_RESERVED
        ).order_by(
            'start'
        )[:5]
        previous_reservations = shop_reservations.filter(
            start__lt=datetime.datetime.now()
        ).order_by('state', '-start')

        shop_schedules = Schedule.objects.filter(
            shop=shop,
            start__gt=datetime.datetime.now()
        )[:5]

        context.update(
            upcoming_reservations=upcoming_reservations,
            previous_reservations=previous_reservations,
            shop_schedules=shop_schedules
        )
        return context


def schedule(request):
    # fixme: replace 1 by shop_id from shop retrieved by barber user_id
    shop = BarberShop.objects.get(id=1)
    if request.method == "POST":
        start_dt = parse_datetime(request.POST.get('start', ''))
        try:
            duration = datetime.timedelta(minutes=int(request.POST.get('duration')))
        except (TypeError, ValueError):
            duration = None
        if not start_dt and duration:
            return HttpResponse('bad request')
        if Schedule.objects.filter(
                Q(start__lte=start_dt, start__gt=start_dt-F('duration')) |
                Q(start__lt=start_dt+duration, start__gte=start_dt-F('duration')) |
                Q(start__gte=start_dt, start__lte=start_dt+duration-F('duration')),
                shop=shop,
        ).exists():
            return HttpResponse("there is an overlap with other free times")

        Schedule.objects.create(shop=shop, start=start_dt, duration=duration)

        return redirect('/barbers/profile/')

    else:
        return render(request, 'barber/new_schedule.html')
