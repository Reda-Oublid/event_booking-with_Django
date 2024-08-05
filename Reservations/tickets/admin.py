from django.contrib import admin

# Register your models here.
# from tickets.models import Event, Reservation
from tickets.models import Event, Reservation

admin.site.register(Event)
admin.site.register(Reservation)
