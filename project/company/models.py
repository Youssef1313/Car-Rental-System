from django.db import models
from django.contrib.auth import get_user_model

class CarStatus(models.TextChoices):
    ACTIVE = 'A', 'Active'
    OUT_OF_SERVICE = 'OOS', 'Out of service'

class Car(models.Model):
    plate_id = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()

    status = models.CharField(max_length=8, choices=CarStatus.choices)

class Customer(models.Model):
    customer_id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()
    email = models.EmailField()
    password = models.TextField()
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)

class Reservation(models.Model):
    reservation_id = models.PositiveIntegerField(primary_key=True)
    date = models.DateTimeField()
    customer = models.ForeignKey(Customer ,related_name='reservation', on_delete=models.CASCADE)
    car = models.ForeignKey(Car ,related_name='reservation', on_delete=models.CASCADE)
