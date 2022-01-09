from django.db.models import Q
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Office


def offices(request):
    if 'value' in request.GET:
        val = request.GET['value']
        mult_search = Q(Q(id__icontains=val)|
                         Q(office_name__icontains=val)|
                         Q(office_location__icontains=val))
        
        offices = Office.objects.filter(mult_search)
    else:
        offices = Office.objects.all()
    return render(request, "offices/offices.html", {"offices": offices, "title": "Our offices"})


def edit_office(request, office_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    office = Office.objects.get(pk=office_id)
    if request.method == "GET":
        return render(request, "offices/edit_office.html", {'office': office, 'title': 'Edit office'})
    elif request.method == "POST":
        office.office_name = request.POST.get('office_name')
        office.office_location = request.POST.get('office_location')
        office.save()
        return redirect(offices)


def add_office(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    if request.method == "GET":
        return render(request,"offices/add_office.html",{'title' : 'Add Office'})

    elif request.method == "POST":
        office_name = request.POST['office_name']
        office_location = request.POST['office_location']
    
        office = Office(
            office_name=office_name,
            office_location=office_location,
        )
        office.save()
    return redirect(offices)


def details(request, office_id):
    office = Office.objects.get(pk=office_id)
    return render(request, "offices/office_details.html", {'office': office, 'title': 'Office details'})
