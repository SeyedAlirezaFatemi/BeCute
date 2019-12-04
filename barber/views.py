import datetime

from django.db.models import Q, F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import generic

from BeCute.misc import parse_datetime
from account.models import CustomUser
from barber.models import Schedule, BarberShop
from customer.models import Reservation


def main(request):
    return render(request, "barber/index.html", context={})


class BarberProfileView(generic.TemplateView):
    template_name = "barber/profile.html"

    def get_context_data(self, **kwargs):
        context = super(BarberProfileView, self).get_context_data(**kwargs)

        shop = BarberShop.objects.get(
            barber=CustomUser.objects.get(username=self.request.user.username)
        )

        shop_reservations = Reservation.objects.filter(shop=shop)
        upcoming_reservations = shop_reservations.filter(
            state=Reservation.STATE_RESERVED
        ).order_by("start")[:5]
        previous_reservations = shop_reservations.filter(
            start__lt=datetime.datetime.now()
        ).order_by("state", "-start")

        shop_schedules = Schedule.objects.filter(
            shop=shop,
            # start__gt=datetime.datetime.now()
        )[:5]

        context.update(
            upcoming_reservations=upcoming_reservations,
            previous_reservations=previous_reservations,
            shop_schedules=shop_schedules,
        )
        return context


def schedule(request):
    try:
        shop = BarberShop.objects.get(barber=request.user)
    except BarberShop.DoesNotExist:
        return HttpResponse("bad request.")
    if request.method == "POST":
        start_dt = parse_datetime(request.POST.get("start", ""))
        try:
            duration = datetime.timedelta(minutes=int(request.POST.get("duration")))
        except (TypeError, ValueError):
            duration = None
        if not start_dt and duration:
            return HttpResponse("bad request")
        if Schedule.objects.filter(
            Q(start__lte=start_dt, start__gt=start_dt - F("duration"))
            | Q(start__lt=start_dt + duration, start__gte=start_dt - F("duration"))
            | Q(start__gte=start_dt, start__lte=start_dt + duration - F("duration")),
            shop=shop,
        ).exists():
            return HttpResponse("there is an overlap with other free times")

        Schedule.objects.create(shop=shop, start=start_dt, duration=duration)

        return redirect("/barbers/profile/")

    else:
        return render(request, "barber/new_schedule.html")


def cancel_schedule(request, schedule_id):
    schedule_to_be_deleted = Schedule.objects.filter(
        id=schedule_id, shop__barber=request.user
    ).first()
    if schedule_to_be_deleted:
        if Reservation.objects.filter(
            shop=schedule_to_be_deleted.shop,
            start__gt=schedule_to_be_deleted.start,
            start__lt=schedule_to_be_deleted.start + schedule_to_be_deleted.duration,
            state=Reservation.STATE_RESERVED,
        ).exists():
            return HttpResponse("There are reservations in this time.")
        schedule_to_be_deleted.delete()
    return redirect("/barbers/profile")
