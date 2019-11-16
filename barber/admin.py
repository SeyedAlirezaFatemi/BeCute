from django.contrib import admin

from barber.models import *

admin.site.register(Service)
admin.site.register(Schedule)
admin.site.register(BarberShop)
admin.site.register(BarberService)
