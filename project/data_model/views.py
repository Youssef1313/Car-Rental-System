from django.shortcuts import render
from rest_framework.response import Response
from .models import Car ,Customer ,Reservation
from rest_framework.decorators import api_view
from .serializers import CarSerializers ,CustomerSerializers ,ReservationSerializers
from rest_framework import status, filters
# List = GET
# Create = POST
# pk query = GET
# Update = PUT
# Delete (Destroy) = DELETE 

@api_view(['GET' ,'POST'])
def fn_list(request):

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



# @api_view
# def 