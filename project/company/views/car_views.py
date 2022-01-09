from django.db.models import Q
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Car, CarStatus, Office, Reservation


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
