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
from . import views as root_view
from company import views as app_view


urlpatterns = [
    path('', root_view.home, name="home"),
    path('admin/', admin.site.urls, name="admin"),
    path('customers/', app_view.customers, name="customers"),
    path('cars/', app_view.cars, name="cars"),
    path('reservations/', app_view.reservations, name="reservations"),
    path('rest/Cars/', app_view.post_get),
    path('rest/Car/<int:plate_id>/', app_view.get_put_delete),
]
