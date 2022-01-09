from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from ..models import Customer


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
