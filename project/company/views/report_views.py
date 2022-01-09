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

    customer_id = request.GET['customer_id']
    reservation = Reservation.objects.filter(customer__id = customer_id)
    return render(request, "report/customer_reservation.html", {{reservation:"reservation", "title":"CustomerReservation"}})

def payments_specific_period(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    start_date = request.GET['start_date']
    end_date = request.GET['end_date']
    payments =  Payment.objects.filter(payment_date__range=(start_date, end_date)).values("payment_date").annotate(Sum('payment_amount'))
    return render(request, "report/payment.html", {payments:"payments", "title":"Payment"})
