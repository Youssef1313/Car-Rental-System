from datetime import datetime, timedelta
from django.db.models import Sum, Max
from django.db.models.fields import DateField
from django.db.models.functions import Cast
from django.http.response import HttpResponseForbidden
from django.shortcuts import redirect, render

from company.views.reservation_views import reservations
from ..models import Reservation, Payment, CarStatusChangeLog, Car, CarStatus


def specific_customer_reserve(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
        
    reservations = None
    if 'customer_id' in request.GET:
        customer_id = request.GET['customer_id']
        reservations = Reservation.objects.filter(customer__id = customer_id)

    return render(request, "reports/customer_reservation.html", {"reservations":reservations, "title":"Customer reservation"})

def payments_specific_period(request):
    if not request.user.is_superuser:
        return HttpResponseForbidden()
    payments = None
    if 'start_date' in request.GET:
        start_date = datetime.fromisoformat(request.GET['start_date'])
        end_date = datetime.fromisoformat(request.GET['end_date']) + timedelta(days=1)
        payments =  Payment.objects.filter(payment_date__gte=start_date, payment_date__lt=end_date).annotate(payment_date_only = Cast('payment_date', output_field=DateField())).values('payment_date_only').annotate(total_payment_amount=Sum('payment_amount'))

    return render(request, "reports/payment.html", {"payments": payments, "title": "Payment"})


def reports(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    return render(request , "reports/report.html" , {'report' : reports , 'title' : 'Reports'} )

def reservations_within_a_period(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    if 'from_date' in request.GET:
        from_date = datetime.fromisoformat(request.GET['from_date'])
        to_date = datetime.fromisoformat(request.GET['to_date'])
        reservations = Reservation.objects.filter(
            rental_date__gte=from_date,
            rental_date__lt=to_date + timedelta(days=1)
        )
    else:
        reservations = None

    return render(request , "reports/reservations_within_a_period.html" , {'title' : 'Customer reservations in a given period', 'reservations': reservations})

def car_reservations_with_a_period(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    if "from_date" in request.GET:
        from_date = datetime.fromisoformat(request.GET['from_date'])
        to_date = datetime.fromisoformat(request.GET['to_date'])
        car_reservations = Reservation.objects.filter(
            rental_date__gte = from_date,
            rental_date__lt = to_date + timedelta(days=1)
            )
    else:
        car_reservations = None
    return render(request, 'reports/car_reservations_report.html', {'title' : 'Cars Reservations in a given period' , 'reservations': car_reservations})

def status_report(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseForbidden()

    cars = None
    if "search_status_date" in request.GET:
        date = datetime.fromisoformat(request.GET['search_status_date'])
        # SELECT * FROM Status S, Cars C WHERE day < ... 
        #status = CarStatusChangeLog.objects.filter(day__lte = date).values('car').annotate(max_day=Max('day'))
        #cars = Car.objects.filter(statuses__day__lte = date).values('plate_id').annotate(max_day=Max(('statuses__day'))).values('plate_id', 'statuses__id','max_day')
        changelogs = CarStatusChangeLog.objects.raw("SELECT `company_carstatuschangelog`.`id`, `company_carstatuschangelog`.`day`, `company_carstatuschangelog`.`car_id`, `company_carstatus`.`name` FROM `company_carstatuschangelog`, `company_carstatus` WHERE `company_carstatus`.`id` = `company_carstatuschangelog`.`new_status_id`AND `company_carstatuschangelog`.`day` IN(SELECT MAX(`company_carstatuschangelog`.`day`) FROM `company_carstatuschangelog` WHERE `company_carstatuschangelog`.`day` <= '2022-01-12' GROUP BY `company_carstatuschangelog`.`car_id` );")
    return render(request, 'reports/status.html',{'changelogs': changelogs, 'title':'Report'})

# SELECT `carstatuschangelog`.`id`, `carstatuschangelog`.`car_id`, `carstatuschangelog`.`day`, `carstatuschangelog`.`new_status_id`,
#           MAX(`company_carstatuschangelog`.`day`) AS `max_day`
#           FROM `company_carstatuschangelog` WHERE `company_carstatuschangelog`.`day` <= 2022-01-11 GROUP BY `company_carstatuschangelog`.`id` 

# SELECT `company_carstatuschangelog`.`id`, `company_carstatuschangelog`.`car_id`,
#           `company_carstatuschangelog`.`day`, `company_carstatuschangelog`.`new_status_id`, MAX(`company_carstatuschangelog`.`day`) AS `max_day`
#       FROM `company_carstatuschangelog` WHERE `company_carstatuschangelog`.`day` <= 2022-01-11 GROUP BY `company_carstatuschangelog`.`id`