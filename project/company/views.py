from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect, render
from rest_framework.response import Response
from .models import Car, Customer, Reservation
from rest_framework.decorators import api_view
from .serializers import CarSerializers, CustomerSerializers, ReservationSerializers
from rest_framework import status, filters
from company import serializers

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
    cars = Car.objects.all()
    return render(request, "cars.html", {"cars": cars})


def reservations(request):
    reservations = Reservation.objects.all()
    return render(request, "reservations.html", {"reservations": reservations})

def login_customer(request):
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
