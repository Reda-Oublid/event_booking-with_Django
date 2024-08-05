from django import forms
from .models import Reservation, Event
from datetime import date
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['num_tickets']


class EventForm(forms.ModelForm):
    date = forms.DateField(initial=date.today())  # Set default value to current date

    class Meta:
        model = Event
        fields = ['title', 'description', 'date', 'price', 'capacity', 'remaining_tickets']
