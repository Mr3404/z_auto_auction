from django.db import models
from django.contrib.auth.models import User
from auction.models import Vehicle


class Reminder(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    reminder_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reminder for {self.user.username} about {self.vehicle.model.model} at {self.reminder_time}"