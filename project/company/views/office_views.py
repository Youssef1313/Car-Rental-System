from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect, render
from ..models import Office


def offices(request):
    search_dictionary = {}
    if 'search_id' in request.GET:
        search_id = request.GET['search_id']
        search_name = request.GET['search_name']
        search_location = request.GET['search_location']

        mult_search = Q(Q(id__icontains = search_id)&
                         Q(office_name__icontains = search_name)&
                         Q(office_location__icontains = search_location))
        
        offices = Office.objects.filter(mult_search)
        search_dictionary = { "id": search_id, "name": search_name, "location": search_location }
    else:
        offices = Office.objects.all()
    return render(request, "offices/offices.html", {"offices": offices, "title": "Our offices", "search_dictionary": search_dictionary})


def edit_office(request, office_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        messages.success(request, 'Only admin users can edit an office.')
        return redirect(offices)

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
        messages.success(request, 'Only admin users can add an office.')
        return redirect(offices)

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
