from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.IntegerField()
    remaining_tickets = models.IntegerField()

    def __str__(self):
        return self.title


class Reservation(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    num_tickets = models.IntegerField()
    reservation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} reserved {self.num_tickets} tickets for {self.event.title}"
