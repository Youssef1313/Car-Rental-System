from datetime import datetime
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Reservation, CarStatusConstants, Car


# TODO: This view is not yet used..
def reservation_admin(request):
    if 'reservation_search' in request.GET:
        val = request.GET['reservation_search']

        ## TODO Add Customer Id or Customer Name
        mult_search = Q(Q(id__icontains=val)|
                         Q(rental_date__icontains=val)|
                         Q(pickup_date__icontains=val)|
                         Q(return_date__icontains=val)|
                         Q(car__plate_id__icontains=val)|
                         Q(payment__id__icontains=val))
        
        reservations = Reservation.objects.filter(mult_search)
    else:
        reservations = Reservation.objects.all()
    return render(request, "reservation_admin.html", {"reservations": reservations, "title": "Reservations"})


def reservations(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.user.is_superuser:
        reservations = Reservation.objects.all()
    else:
        # Try to test request.user.reservations and see if that works.
        reservations = request.user.reservations.all()
    return render(request, "reservations.html", {"reservations": reservations, "title": "Reservations"})

def reserve_car(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        plate_id = request.POST.get('plate_id')
        with transaction.atomic():
            car = Car.objects.select_for_update().get(pk=plate_id)
            if car.is_reserved:
                messages.info(request, 'Sorry, someone else has already reserved this car.')
                return redirect('cars')
            if car.status.id != CarStatusConstants.ACTIVE_ID:
                messages.info(request, f'Sorry, this car is currently {car.status.name}')
                return redirect('cars')

            reservation = Reservation(rental_date=datetime.now(), customer=request.user, car=car)
            car.is_reserved = True
            car.save()
            reservation.save()
            return redirect('reservations')
