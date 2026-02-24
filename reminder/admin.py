from django.contrib import admin
from .models import Reminder


@admin.register(Reminder)
class ReminderAdmin(admin.ModelAdmin):
    list_display = ('vehicle__vin', 'vehicle', 'user', 'reminder_time')
    list_filter = ('reminder_time',)
    search_fields = ('user__username', 'vehicle__vin')
    