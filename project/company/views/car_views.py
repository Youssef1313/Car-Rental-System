from django.contrib import messages
from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Car, CarStatus, Office


def cars(request):
    if 'search_plate_id' in request.GET:
        search_plate_id = request.GET['search_plate_id']
        search_model = request.GET['search_model']
        search_color = request.GET['search_color']
        search_year = request.GET['search_year']
        search_office_name = request.GET['search_office_name']
        search_office_location = request.GET['search_office_location']

        is_reserved = request.GET['search_is_reserved'] == '' or request.GET['search_is_reserved'] == 'true'
        mult_search = Q(Q(plate_id__icontains=search_plate_id) &
                        Q(model__icontains=search_model) &
                        Q(color__icontains=search_color) &
                        Q(year__icontains=search_year) &
                        Q(belong_office__office_name__icontains=search_office_name) &
                        Q(belong_office__office_location__icontains=search_office_location) &
                        Q(is_reserved=is_reserved))

        if request.GET['car_status'] != '':
            mult_search = mult_search & Q(status__id=request.GET['car_status'])

        cars = Car.objects.filter(mult_search)
    else:
        cars = Car.objects.all()
    car_statuses = CarStatus.objects.all()
    return render(request, "cars/cars.html", {"cars": cars, "car_statuses": car_statuses, "title": "Cars"})


def edit_car(request, plate_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    car = Car.objects.get(pk=plate_id)
    if request.method == "GET":
        car_statuses = CarStatus.objects.all()
        return render(request, "cars/edit_car.html", {'car': car, 'title': 'Edit car', 'car_statuses': car_statuses})
    elif request.method == "POST":
        car.model = request.POST.get('model')
        car.color = request.POST.get('color')
        car.year = request.POST.get('year')
        car.status = CarStatus(id=request.POST.get('car_status'))
        car.save()
        return redirect(cars)


def add_car(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.success(request, 'Only admin users can add cars.')
        return redirect(cars)

    if request.method == "GET":
        car_statuses = CarStatus.objects.all()
        offices = Office.objects.all()
        return render(request,"cars/add_car.html", {'title' : 'Add Car', 'car_statuses': car_statuses, 'offices': offices})

    elif request.method == "POST":
        plate_id = request.POST['plate_id']
        model = request.POST['model']
        color = request.POST['color']
        year = request.POST['year']
        status = CarStatus.objects.get(pk=request.POST['status'])
        belong_office = Office.objects.get(pk=request.POST['office'])
        existing_car = Car.objects.filter(pk=plate_id).first()
        new_car = Car(
            plate_id = plate_id,
            model = model,
            color = color,
            year = year,
            status = status,
            belong_office = belong_office,
        )

        if existing_car is not None:
            messages.success(request, "A car with this plate id already exists")
            return redirect(add_car, {'car': new_car})

        new_car.save()
    return redirect(cars)


def details(request, plate_id):
    car = Car.objects.get(pk=plate_id)
    return render(request, "cars/car_details.html", {'car': car, 'title': 'Car details'})
