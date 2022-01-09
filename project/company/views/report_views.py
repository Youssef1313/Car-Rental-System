from datetime import datetime, timedelta
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Reservation, CarStatusConstants, Car, Payment

def specific_customer_reserve(request):
    pass

def payments_specific_period(request):
    pass

def reports(request):
    return render(request , "reports/report.html" , {'report' : reports , 'title' : 'Reports'} )

def reservations_within_a_period(request):
    from_date = datetime.fromisoformat(request.GET['from_date'])
    to_date = datetime.fromisoformat(request.GET['to_date'])
    reservations = Reservation.objects.filter(
        rental_date__gte=from_date,
        rental_date__lt=to_date + timedelta(days=1)
    )
    return render(request , "reports/reservations_within_a_period.html" , {'title' : 'Customer reservations in a given period', 'reservations': reservations})
