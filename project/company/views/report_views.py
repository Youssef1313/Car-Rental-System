from datetime import datetime, timedelta
from django.contrib import messages
from django.db import transaction
from django.db.models import Q,Sum
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Customer, Reservation, CarStatusConstants, Car, Payment

def specific_customer_reserve(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
        
    customer_id = request['customer_id']
    reservation = Reservation.objects.filter(customer_id = customer_id)
    return render(request, "reports/report/customer_reservation.html", {{reservation:"reservation", "title":"CustomerReservation"}})

def payments_specific_period(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    start_date = request['start_date']
    end_date = request['end_date']
    reservation =  Reservation.objects.filter(pub_date__range=(start_date, end_date))
    total_payment = reservation.filter(field_name__isnull=True).aggregate(Sum('payment_id__payment_amount'))
    return render(request, "reports/report/payment.html", {reservation:"reservation", total_payment:"total_payment", "title":"Payment"})
