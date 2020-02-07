import datetime

from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from BeCute.misc import parse_datetime
from account.models import CustomUser
from barber.models import Schedule, BarberShop, Service, BarberService
from customer.forms import CommentForm
from customer.models import Reservation, Comment


# from django.views.generic.edit import CreateView


def main(request):
    print("customer index")
    request.session['user_type'] = 'customer'
    request.session['page'] = 'profile'
    return render(request, "customer/index.html", context={})


class CreateComment(CreateView):
    template_name = "customer/comment.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse('barber_info', kwargs={'barbershop_id': self.barbershop_name})

    def dispatch(self, request, *args, **kwargs):
        self.barbershop_name = kwargs['barbershop_name']
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateComment, self).get_form_kwargs()
        barber_shop = BarberShop.objects.get(name=self.barbershop_name)
        kwargs.update({'request': self.request, 'barbershop': barber_shop})
        return kwargs


def reserve(request):
    request.session['user_type'] = 'customer'
    request.session['page'] = 'reserve'
    if request.method == "POST":
        start = parse_datetime(request.POST.get("start", ""))
        try:
            shop = BarberShop.objects.get(id=int(request.POST.get("shop_id")))
            service_name = str(request.POST.get("id_service"))
            service = shop.service.get(id=service_name)
            duration = service.duration
        except (TypeError, ValueError, BarberShop.DoesNotExist):
            shop = None
            duration = None
        if not (start and duration and shop):
            # return HttpResponse("bad request NONE")
            request.session['user_type'] = 'customer'
            request.session['error_message'] = 'Bad Request!'
            return redirect("/error/")

        if (
            Reservation.objects.filter(
                shop=shop, start__lt=start + duration, start__gte=start - F("duration")
            ).exists()
            or not Schedule.objects.filter(
            shop=shop, start__lte=start, start__gte=start + duration - F("duration")
        ).exists()
        ):
            # return HttpResponse("requested time is not available")
            request.session['user_type'] = 'customer'
            request.session['error_message'] = 'Requested time is not available!'
            return redirect("/error/")

        Reservation.objects.create(
            shop=shop,
            customer=request.user,
            duration=duration,
            start=start,
            state=Reservation.STATE_RESERVED,
            service=service
        )

        return redirect("/customers/profile")

    else:
        shops = BarberShop.objects.values_list("id", "name")
        return render(request, "customer/new_reservation.html", {"shops": shops})


def cancel(request, reserve_id):
    request.session['user_type'] = 'customer'
    request.session['page'] = 'cancel'
    Reservation.objects.filter(id=reserve_id, customer=request.user).delete()
    return redirect("/customers/profile")


def search(request):
    # if request.method == 'GET':
    #     body = json.loads(request.body)
    #     point = Point(body["long"], body["latt"])

    # search_result = BarberShop.objects.annotate(
    #     distance=Distance('location', point)
    # ).order_by('distance').all()

    # return HttpResponse(json.dumps(search_result))
    request.session['user_type'] = 'customer'
    request.session['page'] = 'search'
    return HttpResponse(" this is search page of costumer")


class CustomerProfileView(TemplateView):
    template_name = "customer/profile.html"

    def get_context_data(self, **kwargs):
        self.request.session['user_type'] = 'customer'
        self.request.session['page'] = 'profile'
        context = super(CustomerProfileView, self).get_context_data(**kwargs)
        user_reservations = Reservation.objects.filter(customer=self.request.user)
        upcoming_reservations = user_reservations.filter(
            state=Reservation.STATE_RESERVED,
            start__gte=datetime.datetime.now()
        ).order_by("start")[:3]
        previous_reservations = user_reservations.filter(
            start__lt=datetime.datetime.now()
        ).order_by("state", "-start")
        context.update(
            upcoming_reservations=upcoming_reservations,
            previous_reservations=previous_reservations,
        )
        return context


def profile(request, customer_username):
    # if request.session['user_type'] == 'customer':
    #     request.session['user_type'] = 'customer'
    #     request.session['page'] = 'profile'
    request.session['page'] = 'profile_visit'
    customer = CustomUser.objects.get(
        username=customer_username
    )

    return render(request, 'customer/info.html', {'customer': customer})


def load_services(request):
    request.session['user_type'] = 'customer'
    request.session['page'] = 'load_services'
    shop_id = request.GET.get('shop_id')
    barbershop = BarberShop.objects.filter(id=shop_id)
    barbershop = list(set(barbershop))[0]
    services = barbershop.service.all()
    return render(request, 'customer/services_dropdown.html', {'services': services})


def load_services_list(request):
    request.session['user_type'] = 'customer'
    request.session['page'] = 'load_services_list'
    shop_id = request.GET.get('shop_id')
    barbershop = BarberShop.objects.filter(id=shop_id)
    barbershop = list(set(barbershop))[0]
    services = barbershop.service.all()
    return render(request, 'customer/services_table.html', {'services': services})


class RatingAndObject():
    def __init__(self, object, rating):
        self.barbershop = object
        self.rating = rating
        self.int_rating = int(rating)


class RatingAndObjectAndServices():
    def __init__(self, object, rating, services):
        self.barbershop = object
        self.rating = rating
        self.int_rating = int(rating)
        self.discounted_services = services


def explore(request):
    request.session['user_type'] = 'customer'
    request.session['page'] = 'search'
    return render(request, 'customer/explore.html')


def explore_all(request):
    request.session['user_type'] = 'customer'
    request.session['page'] = 'search'
    all_barbershops = list(BarberShop.objects.all())
    list_of_barbershops = []
    for barbershop in all_barbershops:
        my_comments_list = list(Comment.objects.filter(barbershop=barbershop))
        rating = 0
        for comment in my_comments_list:
            rating += comment.rate
        if len(my_comments_list) != 0:
            rating /= len(my_comments_list)
        else:
            rating = 0
        list_of_barbershops.append(RatingAndObject(barbershop, rating))
    list_of_barbershops.sort(key=lambda x: x.rating, reverse=True)
    return render(request, 'customer/explore_all_table.html', {'list_of_barbershops': list_of_barbershops})


def explore_discount_givers(request):
    request.session['user_type'] = 'customer'
    request.session['page'] = 'search'
    all_barbershops = list(BarberShop.objects.all())
    list_of_barbershops = []
    for barbershop in all_barbershops:
        my_comments_list = list(Comment.objects.filter(barbershop=barbershop))
        rating = 0
        for comment in my_comments_list:
            rating += comment.rate
        if len(my_comments_list) != 0:
            rating /= len(my_comments_list)
        else:
            rating = 0
        list_of_barbershops.append(RatingAndObject(barbershop, rating))
    list_of_barbershops.sort(key=lambda x: x.rating, reverse=True)
    list_of_discounted_barbershops = []
    for barbershop_obj in list_of_barbershops:
        flag = False
        services = []
        services_barbershop = list(BarberService.objects.filter(shop=barbershop_obj.barbershop))
        services_barbershop2 = []
        for s in services_barbershop:
            services_barbershop2.append(s.service)
        for service in services_barbershop2:
            if service.discounted_price != 0:
                services.append(service)
                flag = True
        if flag:
            list_of_discounted_barbershops.append(RatingAndObjectAndServices(barbershop_obj.barbershop, barbershop_obj.rating, services))
    # print(list_of_discounted_barbershops[0].rating)
    return render(request, 'customer/explore_discount_table.html', {'list_of_discounted_barbershops': list_of_discounted_barbershops})
