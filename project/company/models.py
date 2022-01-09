from django.db import models
from django.contrib.auth.models import AbstractUser


class CarStatusConstants:
    # NEVER change these values.
    ACTIVE_ID = 1
    OUT_OF_SERVICE_ID = 2


class CarStatus(models.Model):
    id = models.SmallIntegerField(primary_key=True)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name
    


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    payment_date = models.DateTimeField()
    payment_amount = models.PositiveIntegerField()


class Office(models.Model):
    id = models.AutoField(primary_key=True)
    office_name = models.CharField(max_length=256)
    office_location = models.CharField(max_length=256)

    def __str__(self):
        return self.office_name
    

class Car(models.Model):
    plate_id = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=256)
    color = models.CharField(max_length=64)
    year = models.PositiveSmallIntegerField()
    status = models.ForeignKey(CarStatus, related_name='cars', on_delete=models.RESTRICT)
    belong_office = models.ForeignKey(Office, related_name='cars', on_delete=models.CASCADE)
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.plate_id} {self.belong_office.office_name} {self.status.name}'
    

class Customer(AbstractUser):
    pass

class Reservation(models.Model):
    id = models.AutoField(primary_key=True)
    rental_date = models.DateTimeField()
    pickup_date = models.DateTimeField(null=True)
    return_date = models.DateTimeField(null=True)
    customer = models.ForeignKey(Customer, related_name='reservations', on_delete=models.RESTRICT)
    car = models.ForeignKey(Car, related_name='reservations', on_delete=models.SET_NULL, null=True)
    payment = models.OneToOneField(Payment, related_name='reservation', on_delete=models.RESTRICT, null=True)

    def __str__(self):
        return self.id

class CarStatusChangeLog(models.Model):
    car = models.ForeignKey(Car, related_name="statuses", on_delete=models.CASCADE)
    day = models.DateField()
    new_status = models.ForeignKey(CarStatus, on_delete=models.RESTRICT)
