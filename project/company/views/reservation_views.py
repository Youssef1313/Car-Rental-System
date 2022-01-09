from datetime import datetime, timedelta
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Reservation, CarStatusConstants, Car, Payment



def reservations(request):
    if not request.user.is_authenticated:
        return redirect("login")        

    if request.user.is_superuser:
        if 'search_rental_date' in request.GET:
            search_plate_id = request.GET['search_plate_id']
            search_customer_id = request.GET['search_customer_id']
            search_rental_date = request.GET['search_rental_date']
            mult_search = Q(Q(customer__id__icontains=search_customer_id)&
                             Q(car__plate_id__icontains=search_plate_id))
            if search_rental_date != '':
                mult_search = mult_search & Q(rental_date__lt=datetime.fromisoformat(search_rental_date) + timedelta(days=1))

            reservations = Reservation.objects.filter(mult_search)
        else:
            reservations = Reservation.objects.all()
    else:
        if 'search_rental_date' in request.GET:
            search_plate_id = request.GET['search_plate_id']
            search_rental_date = request.GET['search_rental_date']
            mult_search = Q(car__plate_id__icontains=search_plate_id)
            if search_rental_date != '':
                mult_search = mult_search & Q(rental_date__lt=datetime.fromisoformat(search_rental_date) + timedelta(days=1))
            
            reservations = request.user.reservations.filter(mult_search)
        else:
            reservations = request.user.reservations.all()

    return render(request, "reservations/reservations.html", {"reservations": reservations, "title": "Reservations"})


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


def details(request, reservation_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    reservation = Reservation.objects.get(pk=reservation_id)
    if not request.user.is_superuser and reservation.customer.id != request.user.id:
        return HttpResponseForbidden()

    return render(request, "reservations/reservation_details.html", {'reservation': reservation, 'title': 'Reservation details'})


def pickup_reservation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    reservation = Reservation.objects.get(pk=request.POST["reservation_id"])
    if reservation.pickup_date is not None:
        return HttpResponseBadRequest()

    reservation.pickup_date = datetime.now()
    reservation.save()
    return redirect(details, reservation_id=reservation.id)


def return_reservation(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    reservation = Reservation.objects.get(pk=request.POST["reservation_id"])
    if reservation.return_date is not None or reservation.pickup_date is None:
        return HttpResponseBadRequest()

    reservation.return_date = datetime.now()
    reservation.save()
    car = reservation.car
    car.is_reserved = False
    car.save()
    return redirect(details, reservation_id=reservation.id)


def make_payment(request, reservation_id):
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    reservation = Reservation.objects.get(pk=reservation_id)
    if reservation.payment is not None:
        return HttpResponseBadRequest()

    if request.method == "GET":
        return render(request, "reservations/make_payment.html", {"reservation": reservation})
    elif request.method == "POST":
        payment_amount = request.POST["payment_amount"]
        payment = Payment(
            payment_date=datetime.now(),
            payment_amount=payment_amount,
        )
        reservation.payment = payment
        payment.save()
        reservation.save()
        return redirect(details, reservation_id=reservation_id)
