from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer , Car , Reservation


class CarAdmin(admin.ModelAdmin):
    list_display = ('plate_id' , 'model' , 'color' , 'year' , 'status' ,
                     'belong_office' , 'is_reserved')

    search_fields = ('model' , 'color' , 'year')
    list_filter = ('is_reserved' ,)


class ReservationsAdmin(admin.ModelAdmin):
    list_display = ('id' , 'rental_date' , 'pickup_date' , 'return_date' ,
                         'customer' , 'car' , 'payment')
    search_fields = ('id' , 'rental_date' , 'customer' , 'car')
    list_filter = ('rental_date' ,)


admin.site.register(Customer, UserAdmin)
admin.site.register(Car,CarAdmin)
admin.site.register(Reservation,ReservationsAdmin)