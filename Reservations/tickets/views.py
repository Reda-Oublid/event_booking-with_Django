from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import Event, Reservation
from .forms import ReservationForm, EventForm, SignupForm, LoginForm
from django.shortcuts import render, redirect, get_object_or_404


# signup page
def user_signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'events/signup.html', {'form': form})


# login page
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('event_list')
    else:
        form = LoginForm()
    return render(request, 'events/login.html', {'form': form})


# logout page
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


# Events Handling
@login_required
def create_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'events/create_event.html', {'form': form})


@login_required  # Ensure that users are authenticated to access this list.
def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)
    return render(request, 'events/event_detail.html', {'event': event})


@login_required
def update_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=event.id)
    else:
        form = EventForm(instance=event)
    return render(request, 'events/update_event.html', {'form': form, 'event': event})


@login_required
def confirm_event_delete(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    reservations = Reservation.objects.filter(event=event)
    if request.method == 'POST':
        event.delete()
        reservations.delete()  # Delete associated reservations
        return redirect('event_list')
    return render(request, 'events/confirm_event_delete.html', {'event': event})


# Reservations
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Reservation
from .forms import ReservationForm


@login_required
def reserve_tickets(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.method == 'POST':
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = request.user
            reservation.event = event
            if event.remaining_tickets >= reservation.num_tickets:
                reservation.save()
                event.remaining_tickets -= reservation.num_tickets
                event.save()
                return redirect('event_detail', event_id=event.id)
            else:
                return render(request, 'events/reservation_error.html', {'event': event})
    else:
        form = ReservationForm()  # Instantiate an empty form

    return render(request, 'events/reserve_tickets.html', {'form': form, 'event': event})

@login_required
def user_reservations(request):
    reservations = Reservation.objects.filter(user=request.user)
    for reservation in reservations:
        reservation.total_price = reservation.event.price * reservation.num_tickets  # Calculate total price
    return render(request, 'events/user_reservations.html', {'reservations': reservations})


@login_required
def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        if form.is_valid():
            form.save()
            return redirect('event_detail', event_id=reservation.event.id)
    else:
        form = ReservationForm(instance=reservation)
    return render(request, 'events/update_reservation.html', {'form': form, 'reservation': reservation})


@login_required
def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)
    if request.method == 'POST':
        # Delete Reservation and update num_tickets
        event = reservation.event
        event.remaining_tickets += reservation.num_tickets
        reservation.total_price = reservation.event.price * reservation.num_tickets  # Calculate total price
        event.save()  # save changes to the event
        reservation.delete()  # delete This reservation

        # success message and redirect to reservations page
        messages.success(request, 'Reservation Deleted with Success')
        return redirect('reservations')
    return render(request, 'events/confirm_reservation_delete.html', {'reservation': reservation})
