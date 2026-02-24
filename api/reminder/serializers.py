from rest_framework import serializers
from reminder.models import Reminder


class ReminderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = ['id', 'user', 'vehicle', 'reminder_time']
        read_only_fields = ['id', 'reminder_time']