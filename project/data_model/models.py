from django.db import models


class Car(models.Model):
    plate_id = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=255)
    year = models.PositiveSmallIntegerField()

    # status
    active = models.BooleanField()
    out_of_service = models.BooleanField()

class Customer(models.Model):
    customer_id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()
    email = models.EmailField()
    password = models.TextField()

class Reservation(models.Model):
    reservation_id = models.PositiveIntegerField(primary_key=True)
    date = models.DateTimeField()
    customer = models.ForeignKey(Customer ,related_name='reservation', on_delete=models.CASCADE)
    car = models.ForeignKey(Car ,related_name='reservation', on_delete=models.CASCADE)