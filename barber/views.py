from django.http import HttpResponse
from django.shortcuts import render

from BeCute.misc import parse_date
from barber.models import Schedule


def main(request):
    return render(request, 'barber/index.html', context={})


def profile(request):
    return HttpResponse(" this is profile page of costumer")


def schedule(request, start=None, end=None):
    if request.method == "POST":
        pass
    else:
        # fixme: replace one by shop_id from shop retrieved by barber user_id
        schedules = Schedule.objects.filter(shop=1, start__gte=parse_date(start), start__lte=parse_date(end)).all()
        return render(request, 'barber/schedule.html', {'schedules': schedules, 'start_time': start, 'end_time': end})
