from django.db import models
from django.contrib.auth.models import AbstractUser

class CarStatus(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64)


class Car(models.Model):
    plate_id = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()
    status = models.ForeignKey(CarStatus, related_name='status', on_delete=models.RESTRICT)

class Customer(AbstractUser):
    pass

class Reservation(models.Model):
    reservation_id = models.PositiveIntegerField(primary_key=True)
    date = models.DateTimeField()
    customer = models.ForeignKey(Customer ,related_name='reservation', on_delete=models.CASCADE)
    car = models.ForeignKey(Car ,related_name='reservation', on_delete=models.CASCADE)

class Payment(models.Model):
    payment_id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField()
    payment_amount = models.PositiveIntegerField()

class Office(models.Model):
    office_id = models.AutoField(primary_key=True)
    office_name = models.CharField(max_length=255)
    office_location = models.CharField(max_length=255)

