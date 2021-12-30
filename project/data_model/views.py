from django.shortcuts import render


def customers(request):
    return render(request, "customers.html")


def cars(request):
    return render(request, "cars.html")


def reservations(request):
    return render(request, "reservations.html")
