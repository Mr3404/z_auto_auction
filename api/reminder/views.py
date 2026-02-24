from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from reminder.models import Reminder
from auction.models import Vehicle
from .serializers import ReminderSerializer


class AddReminderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        vehicle = Vehicle.objects.get(id=data["vehicle"])
        if timezone.now() < vehicle.auction_start_date:
            data["user"] = request.user.id
            if Reminder.objects.filter(user=request.user, vehicle=vehicle):
                return Response({"error": "You have already set a reminder for this vehicle"}, status=status.HTTP_400_BAD_REQUEST)
            serializer = ReminderSerializer(data=data, many=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "Auction has already started"}, status=status.HTTP_400_BAD_REQUEST)