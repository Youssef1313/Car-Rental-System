from datetime import datetime, timedelta
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http.response import HttpResponseBadRequest, HttpResponseForbidden
from django.shortcuts import redirect, render
from ..models import Reservation, CarStatusConstants, Car, Payment

def specific_customer_reserve(request):
    pass

def payments_specific_period(request):
    pass