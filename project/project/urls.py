"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from company.views import auth_views, car_views, customer_views, report_views, reservation_views, office_views


urlpatterns = [
    path('', views.home, name="home"),
    path('admin/', admin.site.urls, name="admin"),

    # path('api/cars/', app_view.post_get),
    # path('api/car/<int:plate_id>/', app_view.get_put_delete),

    # Car urls
    path('cars/', car_views.cars, name="cars"),
    path('cars/edit/<int:plate_id>', car_views.edit_car, name="edit_car"),
    path("cars/add/", car_views.add_car, name="add_car"),
    path("cars/details/<int:plate_id>", car_views.details, name="car_details"),

    # Office urls
    path('offices/', office_views.offices, name="offices"),
    path('offices/edit/<int:office_id>', office_views.edit_office, name="edit_office"),
    path("offices/add/", office_views.add_office, name="add_office"),
    path("offices/details/<int:office_id>", office_views.details, name="office_details"),

    # Authentication urls
    path('login/', auth_views.login_customer, name="login"),
    path('signup/', auth_views.signup_customer, name="signup"),
    path('logout/', auth_views.logout_customer, name="logout"),

    # Customer urls
    path('customers/', customer_views.customers, name="customers"),

    # Reservation urls
    path('reservations/', reservation_views.reservations, name="reservations"),
    path('reservations/details/<int:reservation_id>', reservation_views.details, name="reservation_details"),
    path('reservations/pickup/', reservation_views.pickup_reservation, name="pickup_reservation"),
    path('reservations/return/', reservation_views.return_reservation, name="return_reservation"),
    path('reservations/make_payment/<int:reservation_id>', reservation_views.make_payment, name="make_payment"),
    path('reserve/', reservation_views.reserve_car, name="reserve_car"),
    
    #Reports
    path('report/customer_reservation.html', report_views.specific_customer_reserve, name="customer_reservation"),
    path('report/payment.html', report_views.payments_specific_period, name="payment"),


]

