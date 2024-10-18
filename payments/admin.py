from .models import Payment
from django.contrib import admin


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'user', 'amount', 'paid_at')
    
admin.site.register(Payment, PaymentAdmin)