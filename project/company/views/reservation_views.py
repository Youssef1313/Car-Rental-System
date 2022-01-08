from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from ..models import Customer, Reservation


def customers(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    if 'customer_search' in request.GET:
        val = request.GET['customer_search']
        
        ##TODO Change this search attr. with the customer attr
        
        # mult_search = Q(Q(plate_id__icontains=val)|
        #                     Q(model__icontains=val)|
        #                     Q(color__icontains=val)|
        #                     Q(year__icontains=val)|
        #                     Q(belong_office__office_name__icontains=val)|
        #                     Q(belong_office__office_location__icontains=val))
        
        # customers = Customer.objects.filter(mult_search)
    else:
        customers = Customer.objects.all()
    return render(request, "customers.html", {"customers": customers, "title": "Customers"})


def reservation_admin(request):
    if 'reservation_search' in request.GET:
        val = request.GET['reservation_search']

        ## TODO Add Customer Id or Customer Name
        mult_search = Q(Q(id__icontains=val)|
                         Q(rental_date__icontains=val)|
                         Q(pickup_date__icontains=val)|
                         Q(return_date__icontains=val)|
                         Q(car__plate_id__icontains=val)|
                         Q(payment__id__icontains=val))
        
        reservations = Reservation.objects.filter(mult_search)
    else:
        reservations = Reservation.objects.all()
    return render(request, "reservation_admin.html", {"reservations": reservations, "title": "Reservations"})


def reservations(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden()
    if request.user.is_superuser:
        reservations = Reservation.objects.all()
    else:
        # Try to test request.user.reservations and see if that works.
        reservations = Reservation.objects.filter(pk=request.user.id)
    return render(request, "reservations.html", {"reservations": reservations, "title": "Reservations"})
