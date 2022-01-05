from collections import namedtuple
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .forms import SignupForm
from .models import Car, Customer, Office, Reservation
from .serializers import CarSerializers, CustomerSerializers, ReservationSerializers
from django.db.models import Q
# List = GET
# Create = POST
# pk query = GET
# Update = PUT
# Delete (Destroy) = DELETE 

@api_view(['GET', 'POST'])
def post_get(request):

    # 1.GET
    if request.method == 'GET':
        cars = Car.objects.all()
        # print(cars)
        # print('ok')
        serializer = CarSerializers(cars ,many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = CarSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            Response(serializer.data ,status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET','PUT','DELETE'])
def get_put_delete(request, plate_id):
    try:
        car = Car.objects.get(pk=plate_id)
        # Get_Car
        if request.method == 'GET':
            serializer = CarSerializers(car)
            return Response(serializer.data)

        # Put_Car -> Update
        if request.method == 'PUT':
            serializer = CarSerializers(car, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

        # Delete_Car
        if request.method == 'DELETE':
            car.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    except Car.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)



def customers(request):
    customers = Customer.objects.all()
    return render(request, "customers.html", {"customers": customers})

    
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
    return render(request, "cars_customer.html", {"cars": cars})

def get_specific_car(request, attr, val):
    pass

def reservations(request):
    reservations = Reservation.objects.all()
    return render(request, "reservations.html", {"reservations": reservations})

def login_customer(request):
    if (request.user.is_authenticated):
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
        return render(request, "login.html") # , {}

def signup_customer(request):
    if (request.user.is_authenticated):
        return redirect('home')

    if request.method == "POST":
        form = SignupForm(request.POST)
        if (form.is_valid()):
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, "signup.html", {'form': form})

def logout_customer(request):
    logout(request)
    return redirect('home')

