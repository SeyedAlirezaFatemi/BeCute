import datetime

from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, CreateView

from BeCute.misc import parse_datetime
from account.models import CustomUser
from barber.models import Schedule, BarberShop
from customer.forms import CommentForm
from customer.models import Reservation


# from django.views.generic.edit import CreateView


def main(request):
    print("customer index")
    return render(request, "customer/index.html", context={})


class CreateComment(CreateView):
    template_name = "customer/comment.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse('info', kwargs={'barbershop_id': self.barbershop_name})

    def dispatch(self, request, *args, **kwargs):
        self.barbershop_name = kwargs['barbershop_name']
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateComment, self).get_form_kwargs()
        barber_shop = BarberShop.objects.get(name=self.barbershop_name)
        kwargs.update({'request': self.request, 'barbershop': barber_shop})
        return kwargs


def reserve(request):
    if request.method == "POST":
        start = parse_datetime(request.POST.get("start", ""))
        try:
            shop = BarberShop.objects.get(id=int(request.POST.get("shop_id")))
            duration = datetime.timedelta(minutes=int(request.POST.get("duration")))
        except (TypeError, ValueError, BarberShop.DoesNotExist):
            shop = None
            duration = None
        if not (start and duration and shop):
            return HttpResponse("bad request")

        if (
            Reservation.objects.filter(
                shop=shop, start__lt=start + duration, start__gte=start - F("duration")
            ).exists()
            or not Schedule.objects.filter(
            shop=shop, start__lte=start, start__gte=start + duration - F("duration")
        ).exists()
        ):
            return HttpResponse("requested time is not available")

        Reservation.objects.create(
            shop=shop,
            customer=request.user,
            duration=duration,
            start=start,
            state=Reservation.STATE_RESERVED,
        )

        return redirect("/customers/profile")

    else:
        shops = BarberShop.objects.values_list("id", "name")
        return render(request, "customer/new_reservation.html", {"shops": shops})


def cancel(request, reserve_id):
    Reservation.objects.filter(id=reserve_id, customer=request.user).update(
        state=Reservation.STATE_CANCELED
    )
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


class CustomerProfileView(TemplateView):
    template_name = "customer/profile.html"

    def get_context_data(self, **kwargs):
        context = super(CustomerProfileView, self).get_context_data(**kwargs)
        # TODO filter by user
        user_reservations = Reservation.objects.filter()
        upcoming_reservations = user_reservations.filter(
            state=Reservation.STATE_RESERVED
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
    customer = CustomUser.objects.get(
        username=customer_username
    )

    return render(request, 'customer/info.html', {'customer': customer})
