from django.contrib import admin
from .models import Hotel,Room,Booking
# Register your models here.

class HotelAdmin(admin.ModelAdmin):
    list_display = ('hotel_name','address','city','state','pincode',)
    # form = HotelAdminForm
admin.site.register(Hotel,HotelAdmin)

class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_no','hotel_name','room_type','rate','is_available',)
    ordering = ['room_no']
admin.site.register(Room,RoomAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display=('guest','room','hotel','no_of_guests','checkin_date','checkout_date','check_out','charge',)
    # form = BookingAdminForm

admin.site.register(Booking,BookingAdmin)