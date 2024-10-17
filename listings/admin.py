from .models import Listing
from django.contrib import admin

class ListingAdmin(admin.ModelAdmin):
    list_display = ('id', 'make', 'model', 'year', 'body_type', 'status')
    readonly_fields = ('added_at',)


admin.site.register(Listing, ListingAdmin)