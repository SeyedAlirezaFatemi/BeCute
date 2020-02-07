import datetime

from django.db.models import Q, F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic

from BeCute.misc import parse_datetime
from account.models import CustomUser
from barber.models import Schedule, BarberShop, Service, BarberService
from customer.models import Reservation, Comment
from barber.forms import AddServiceToBarbershop


def main(request):
    request.session['user_type'] = 'barber'
    request.session['page'] = 'main'
    return render(request, "barber/index.html", context={})


class NameAndNumber():
    def __init__(self, name, number, number2, object):
        self.name = name
        self.number = number
        self.number2 = number2
        self.object = object


class BarberProfileView(generic.TemplateView):
    template_name = "barber/profile.html"

    def get_context_data(self, **kwargs):
        self.request.session['user_type'] = 'barber'
        self.request.session['page'] = 'profile'
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
        previous_reservations_list = list(previous_reservations)

        loving_customers = {}
        customers = {}
        for reservation in previous_reservations_list:
            if reservation.customer.username in loving_customers.keys():
                loving_customers[reservation.customer.username] += 1
            else:
                loving_customers[reservation.customer.username] = 1
                customers[reservation.customer.username] = reservation.customer
        loving_customers_list_of_values = list(loving_customers.values())
        loving_customers_list_of_values = sorted(loving_customers_list_of_values, reverse=True)

        upcoming_reservations_list = list(upcoming_reservations)
        loving_customers_upcoming = {}
        for reservation in upcoming_reservations_list:
            if reservation.customer.username in loving_customers_upcoming.keys():
                loving_customers_upcoming[reservation.customer.username] += 1
            else:
                loving_customers_upcoming[reservation.customer.username] = 1

        top_customer = []
        for key in loving_customers.keys():
            if len(loving_customers_list_of_values) > 0 and loving_customers[key] == loving_customers_list_of_values[0]:
                if key in loving_customers_upcoming.keys():
                    top_customer.append(NameAndNumber(key, loving_customers[key], loving_customers_upcoming[key], customers[key]))
                else:
                    top_customer.append(NameAndNumber(key, loving_customers[key], 0, customers[key]))

        for key in loving_customers.keys():
            if len(loving_customers_list_of_values) > 1 and loving_customers[key] == loving_customers_list_of_values[1]:
                if key in loving_customers_upcoming.keys():
                    top_customer.append(
                        NameAndNumber(key, loving_customers[key], loving_customers_upcoming[key], customers[key]))
                else:
                    top_customer.append(NameAndNumber(key, loving_customers[key], 0, customers[key]))
        for key in loving_customers.keys():
            if len(loving_customers_list_of_values) > 2 and loving_customers[key] == loving_customers_list_of_values[2]:
                if key in loving_customers_upcoming.keys():
                    top_customer.append(NameAndNumber(key, loving_customers[key], loving_customers_upcoming[key], customers[key]))
                else:
                    top_customer.append(NameAndNumber(key, loving_customers[key], 0, customers[key]))

        top_customer = top_customer[0: min(3, len(top_customer))]

        context.update(
            upcoming_reservations=upcoming_reservations,
            previous_reservations=previous_reservations,
            shop_schedules=shop_schedules,
            barber_name=barber_name,
            top_customer=top_customer,
        )
        return context


def schedule(request):
    request.session['user_type'] = 'barber'
    request.session['page'] = 'schedule'

    try:
        shop = BarberShop.objects.get(barber=request.user)
    except BarberShop.DoesNotExist:
        # return HttpResponse("bad request.")
        request.session['user_type'] = 'barber'
        request.session['error_message'] = 'Bad Request!'
        return redirect("/error/")
    if request.method == "POST":
        start_dt = parse_datetime(request.POST.get("start", ""))
        try:
            duration = datetime.timedelta(minutes=int(request.POST.get("duration")))
        except (TypeError, ValueError):
            duration = None
        if not start_dt and duration:
            # return HttpResponse("bad request")
            request.session['user_type'] = 'barber'
            request.session['error_message'] = 'Bad Request!'
            return redirect("/error/")
        if Schedule.objects.filter(
            Q(start__lte=start_dt, start__gt=start_dt - F("duration"))
            | Q(start__lt=start_dt + duration, start__gte=start_dt - F("duration"))
            | Q(start__gte=start_dt, start__lte=start_dt + duration - F("duration")),
            shop=shop,
        ).exists():
            # return HttpResponse("there is an overlap with other free times")
            request.session['user_type'] = 'barber'
            request.session['error_message'] = 'There is an overlap with other free times!'
            return redirect("/error/")

        Schedule.objects.create(shop=shop, start=start_dt, duration=duration)

        return redirect("/barbers/profile/")

    else:
        return render(request, "barber/new_schedule.html")


def cancel_schedule(request, schedule_id):
    request.session['user_type'] = 'barber'
    request.session['page'] = 'cancel_schedule'
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
            # return HttpResponse("There are reservations in this time.")
            request.session['user_type'] = 'barber'
            request.session['error_message'] = "There are reservations in this time."
            return redirect("/error/")
        schedule_to_be_deleted.delete()
    return redirect("/barbers/profile")


def profile(request, barbershop_id):
    # if not 'user_type' in request.session:
    # if request.session['user_type'] == 'barber':
    #     request.session['user_type'] = 'barber'
    request.session['page'] = 'profile_visit'
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
    total = len(barbershops)

    return render(request, 'barber/info.html', {'barbershop': barbershop, 'shop_comments': comments, 'add_comment': show_comment_form, 'services': services, "rating": round(rating), "rating_exact": rating, "rank": rank, "total_number_of_barbershops": total})


def add_service(request):
    request.session['user_type'] = 'barber'
    request.session['page'] = 'add_service'
    try:
        shop = BarberShop.objects.get(barber=request.user)
    except BarberShop.DoesNotExist:
        # return HttpResponse("bad request.")
        request.session['user_type'] = 'barber'
        request.session['error_message'] = 'Bad Request!'
        return redirect("/error/")
    if request.method == "POST":
        price = request.POST.get("price")
        try:
            price_float = float(price)
            if price_float < 0:
                raise TypeError
        except:
            # return HttpResponse("The price should be valid.")
            # return HttpResponse("bad request.")
            request.session['user_type'] = 'barber'
            request.session['error_message'] = 'The price should be valid!'
            return redirect("/error/")

        try:
            discounted_price = float(request.POST.get("discounted_price"))
            if discounted_price < 0 or discounted_price >= price_float:
                raise TypeError
            # print("hellooooooooooooooo", discounted_price)
        except:
            # discounted_price = 0
            # print("byyyyyyyyyyyy", discounted_price)
            # return HttpResponse("Discounted Price should be valid (zero if no discount)")
            request.session['user_type'] = 'barber'
            request.session['error_message'] = 'Discounted Price should be valid and less than the original (zero if no discount)!'
            return redirect("/error/")

        service_name = request.POST.get("service_name")

        try:
            duration = datetime.timedelta(minutes=int(request.POST.get("duration")))
        except (TypeError, ValueError):
            duration = None

        barber_services = BarberService.objects.filter(Q(shop=shop))
        # print(barber_services)
        for bs in barber_services:
            if bs.service.name == service_name:
                # return HttpResponse("there is a similar service")
                request.session['user_type'] = 'barber'
                request.session['error_message'] = 'There is a similar service!'
                return redirect("/error/")
        service = Service.objects.create(name=service_name, price=float(price), duration=duration, discounted_price=discounted_price)
        BarberService.objects.create(shop=shop, service=service)
        return redirect("barber-profile")

    else:
        return render(request, "barber/new_service.html")


def edit_service(request):
    request.session['user_type'] = 'barber'
    request.session['page'] = 'edit_service'
    try:
        shop = BarberShop.objects.get(barber=request.user)
        services = shop.service.all()
    except BarberShop.DoesNotExist:
        # return HttpResponse("bad request.")
        request.session['user_type'] = 'barber'
        request.session['error_message'] = 'Bad Request!'
        return redirect("/error/")
    if request.method == "POST":
        price = request.POST.get("price")
        try:
            price_float = float(price)
            if price_float < 0:
                raise TypeError
        except:
            request.session['user_type'] = 'barber'
            request.session['error_message'] = 'The price should be valid!'
            return redirect("/error/")

        try:
            discounted_price = float(request.POST.get("discounted_price"))
            if discounted_price < 0 or discounted_price >= price_float:
                raise TypeError
        except:
            request.session['user_type'] = 'barber'
            request.session['error_message'] = 'Discounted Price should be valid and less than the original (zero if no discount)!'
            return redirect("/error/")

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
            # return HttpResponse('No service with that name')
            request.session['user_type'] = 'barber'
            request.session['error_message'] = 'No service with that name!'
            return redirect("/error/")
        service.name = service_new_name
        service.duration = duration
        service.price = price
        service.discounted_price = discounted_price
        service.save()
        return redirect("barber-profile")

    else:
        return render(request, "barber/edit_service.html", {'services': services})