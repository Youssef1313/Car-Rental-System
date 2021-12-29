from django.db import models


class Car(models.Model):
    plate_id = models.PositiveIntegerField(primary_key=True)
    model = models.CharField(max_length=32)
    year = models.PositiveSmallIntegerField()

    # status
    active = models.BooleanField()
    out_of_service = models.BooleanField()


class Customer(models.Model):
    personal_id = models.PositiveIntegerField(primary_key=True)
    name = models.TextField()
    email = models.EmailField()
    password = models.TextField()


class Reservation(models.Model):
    date = models.DateTimeField()
