from django.contrib import admin
from django.utils.html import format_html
from .models import *


@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'category',
        'package',
        'event_date',
        'status'
    )

    list_filter = ('status',)

    search_fields = (
        'user__username',
        'venue'
    )


from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'booking',
        'amount',
        'payment_method',
        'status',
        'created_at'
    )

    list_filter = (
        'status',
        'payment_method'
    )

    search_fields = (
        'booking__name',
    )

admin.site.register(EventCategory)
admin.site.register(Package)
admin.site.register(Staff)
admin.site.register(Gallery)
admin.site.register(Review)
admin.site.register(Contact)