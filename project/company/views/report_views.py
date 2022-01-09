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
        
    if 'customer_id' in request.GET:
        customer_id = request.GET['customer_id']
        reservation = Reservation.objects.filter(customer__id = customer_id)
    else:
        reservation = Reservation.objects.none()

    return render(request, "report/customer_reservation.html", {{reservation:"reservations", "title":"Customer reservation"}})

def payments_specific_period(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()

    if 'start_date' in request.GET:
        start_date = datetime.date(request.GET['start_date'])
        end_date = datetime.date(request.GET['end_date'])
        payments =  Payment.objects.filter(payment_date__range=(start_date, end_date)).values("payment_date").annotate(Sum('payment_amount'))
    else:
        payments = Payment.objects.none()
    return render(request, "report/payment.html", {payments:"payments", "title":"Payment"})


def reports(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    return render(request , "reports/report.html" , {'report' : reports , 'title' : 'Reports'} )

def reservations_within_a_period(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    from_date = datetime.fromisoformat(request.GET['from_date'])
    to_date = datetime.fromisoformat(request.GET['to_date'])
    reservations = Reservation.objects.filter(
        rental_date__gte=from_date,
        rental_date__lt=to_date + timedelta(days=1)
    )

    return render(request , "reports/reservations_within_a_period.html" , {'title' : 'Customer reservations in a given period', 'reservations': reservations})
