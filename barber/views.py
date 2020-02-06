import datetime

from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import generic

from BeCute.misc import parse_datetime
from account.models import CustomUser
from barber.models import Schedule, BarberShop, Service, BarberService
from customer.models import Reservation, Comment
from barber.forms import AddServiceToBarbershop


def main(request):
    return render(request, "barber/index.html", context={})


class BarberProfileView(generic.TemplateView):
    template_name = "barber/profile.html"

    def get_context_data(self, **kwargs):
        context = super(BarberProfileView, self).get_context_data(**kwargs)
        user = self.request.user
        shop = BarberShop.objects.get(
            barber=user
        )

        shop_reservations = Reservation.objects.filter(shop=shop)
        upcoming_reservations = shop_reservations.filter(
            state=Reservation.STATE_RESERVED,
            start__gte=datetime.datetime.now()
        ).order_by("start")[:5]
        previous_reservations = shop_reservations.filter(
            start__lt=datetime.datetime.now()
        ).order_by("state", "-start")

        shop_schedules = Schedule.objects.filter(
            shop=shop,
            start__gte=datetime.datetime.now()
        )[:5]

        barber_name = BarberShop.objects.get(barber=user).name

        context.update(
            upcoming_reservations=upcoming_reservations,
            previous_reservations=previous_reservations,
            shop_schedules=shop_schedules,
            barber_name=barber_name,
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


def profile(request, barbershop_id):
    barbershop = BarberShop.objects.get(
        name=barbershop_id
    )

    comments = Comment.objects.filter(barbershop=barbershop)
    user = request.user
    show_comment_form = False
    if user.type == CustomUser.USER_TYPE_CLIENT:
        show_comment_form = True
    services = barbershop.service.all()
    my_comments_list = list(Comment.objects.filter(barbershop=barbershop))
    rating = 0
    for comment in my_comments_list:
        rating += comment.rate
    if len(my_comments_list) != 0:
        rating /= len(my_comments_list)
    else:
        rating = 0
    barbershops = list(BarberShop.objects.all())
    rank = 1
    for barber_shop in barbershops:
        if barber_shop == barbershop:
            continue
        my_comments_list = list(Comment.objects.filter(barbershop=barber_shop))
        rating_barber_shop = 0
        for comment in my_comments_list:
            rating_barber_shop += comment.rate
        if len(my_comments_list) != 0:
            rating_barber_shop /= len(my_comments_list)
        else:
            rating_barber_shop = 0
        if rating < rating_barber_shop:
            rank += 1
    total = len(barbershops)+1

    return render(request, 'barber/info.html', {'barbershop': barbershop, 'shop_comments': comments, 'add_comment': show_comment_form, 'services': services, "rating": round(rating), "rating_exact": rating, "rank": rank, "total_number_of_barbershops": total})


def add_service(request):
    try:
        shop = BarberShop.objects.get(barber=request.user)
    except BarberShop.DoesNotExist:
        return HttpResponse("bad request.")
    if request.method == "POST":
        price = request.POST.get("price")
        try:
            float(price)
        except:
            return HttpResponse("bad request.")
        service_name = request.POST.get("service_name")
        try:
            duration = datetime.timedelta(minutes=int(request.POST.get("duration")))
        except (TypeError, ValueError):
            duration = None
        barber_services = BarberService.objects.filter(
            Q(shop=shop))
        print(barber_services)
        for bs in barber_services:
            if bs.service.name == service_name:
                return HttpResponse("there is a similar service")
        service = Service.objects.create(name=service_name, price=float(price), duration=duration)
        BarberService.objects.create(shop=shop, service=service)
        return redirect("barber-profile")

    else:
        return render(request, "barber/new_service.html")


def edit_service(request):
    try:
        shop = BarberShop.objects.get(barber=request.user)
        services = shop.service.all()
    except BarberShop.DoesNotExist:
        return HttpResponse("bad request.")
    if request.method == "POST":
        price = request.POST.get("price")
        try:
            float(price)
        except:
            return HttpResponse("bad request.")
        service_name = request.POST.get("service_name")
        service_new_name = request.POST.get("service_new_name")
        try:
            duration = datetime.timedelta(minutes=int(request.POST.get("duration")))
        except (TypeError, ValueError):
            duration = None
        barber_services = BarberService.objects.filter(
            Q(shop=shop))
        service = None
        for bs in barber_services:
            if bs.service.name == service_name:
                service = bs.service
        if service is None:
            return HttpResponse('No service with that name')
        service.name = service_new_name
        service.duration = duration
        service.price = price
        service.save()
        return redirect("barber-profile")

    else:
        return render(request, "barber/edit_service.html", {'services': services})