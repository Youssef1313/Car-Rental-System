from django.shortcuts import render
from .models import Customer, Car, Reservation


def customers(request):
    customers = Customer.objects.all()
    return render(request, "customers.html", {"customers": customers})


def cars(request):
    cars = Car.objects.all()
    return render(request, "cars.html", {"cars": cars})


def reservations(request):
    reservations = Reservation.objects.all()
    return render(request, "reservations.html", {"reservations": reservations})
