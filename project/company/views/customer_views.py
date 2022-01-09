from django.db.models import Q
from django.http.response import HttpResponseForbidden
from django.shortcuts import render
from ..models import Customer



def customers(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    if 'search_id' in request.GET:
        search_id = request.GET['search_id']
        search_username = request.GET['search_username']
        search_first_name = request.GET['search_first_name']
        search_last_name = request.GET['search_last_name']
        search_email = request.GET['search_email']
        # search_superuser = request.GET['search_superuser']

        mult_search = Q(Q(id__icontains=search_id)&
                            Q(username__icontains=search_username)&
                            Q(first_name__icontains=search_first_name)&
                            Q(last_name__icontains=search_last_name)&
                            Q(email__icontains=search_email))
        
        customers = Customer.objects.filter(mult_search)
    else:
        customers = Customer.objects.all()
    return render(request, "customers.html", {"customers": customers, "title": "Customers"})
