from .models import Booking
from django.contrib import admin


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'start_date', 'end_date', 'status')
    readonly_fields = ('created_at',)


admin.site.register(Booking, BookingAdmin)