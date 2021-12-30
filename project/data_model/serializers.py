from django.db import models
from django.db.models import fields
from django.http.response import JsonResponse
from rest_framework import serializers
from data_model.models import Car, Customer, Reservation

class CarSerializers(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['customer_id','name','email','password','reservation']

class ReservationSerializers(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = '__all__'