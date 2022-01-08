from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from .forms import SignupForm
from .models import Car, CarStatus, Customer, Office, Reservation


def customers(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    if 'customer_search' in request.GET:
        val = request.GET['customer_search']
        
        ##TODO Change this search attr. with the customer attr
        
        # mult_search = Q(Q(plate_id__icontains=val)|
        #                     Q(model__icontains=val)|
        #                     Q(color__icontains=val)|
        #                     Q(year__icontains=val)|
        #                     Q(belong_office__office_name__icontains=val)|
        #                     Q(belong_office__office_location__icontains=val))
        
        # customers = Customer.objects.filter(mult_search)
    else:
        customers = Customer.objects.all()
    return render(request, "customers.html", {"customers": customers, "title": "Customers"})


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

def reservations(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.user.is_superuser:
        reservations = Reservation.objects.all()
    else:
        reservations = Reservation.objects.filter(pk=request.user.id)
    return render(request, "reservations.html", {"reservations": reservations, "title": "Reservations"})

def login_customer(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password.')
            return redirect('login')

    elif request.method == "GET":
        return render(request, "login.html", {"title": "Login"})


def signup_customer(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, "signup.html", {'form': form, 'title': 'Sign up'})


def logout_customer(request):
    logout(request)
    return redirect('home')


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
