from datetime import datetime
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Car, CarStatus, CarStatusConstants, Office, Reservation


def cars(request):
    if 'value' in request.GET:
        val = request.GET['value']
        mult_search = Q(Q(plate_id__icontains=val)|
                         Q(model__icontains=val)|
                         Q(color__icontains=val)|
                         Q(year__icontains=val)|
                         Q(belong_office__office_name__icontains=val)|
                         Q(belong_office__office_location__icontains=val))
        
        cars = Car.objects.filter(mult_search)
    else:
        cars = Car.objects.all()
    return render(request, "cars.html", {"cars": cars, "title": "Cars"})


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


def edit_car(request, plate_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    car = Car.objects.get(pk=plate_id)
    if request.method == "GET":
        return render(request, "edit_car.html", {'car': car, 'title': 'Edit car'})
    elif request.method == "POST":
        car.model = request.POST.get('model')
        car.color = request.POST.get('color')
        car.year = request.POST.get('year')
        car.save()
        return redirect(cars)


def add_car(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == "GET":
        return render(request,"add_car.html",{'title' : 'Add Car'})

    elif request.method == "POST":
        plate_id = request.POST['plate_id']
        car = Car.objects.filter(pk=plate_id).first()
        if car is not None:
            return HttpResponseBadRequest()

        model = request.POST['model']
        color = request.POST['color']
        year = request.POST['year']
        status = CarStatus.objects.get(name = request.POST['status'])
        belong_office = Office.objects.get(office_name = request.POST['belong_office'])

        data = Car(
            plate_id = plate_id,
            model = model,
            color = color,
            year = year,
            status = status,
            belong_office = belong_office,
        )
        data.save()
    return redirect(cars)


def details(request, plate_id):
    car = Car.objects.get(pk=plate_id)
    return render(request, "car_details.html", {'car': car, 'title': 'Car details'})
