from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from auction.models import *
from .serializers import *
from .services import *


class VehicleBrandView(APIView):

    def get(self,request):
        try:
            brands = VehicleBrand.objects.all()
            serializer = VehicleBrandSerializer(brands, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        

class VehicleModelView(APIView):

    def get(self, request):
        try:
            models = VehicleModel.objects.all()
            serializer = VehicleModelSerializer(models, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        

class VehicleListView(APIView):

    def get(self, request):
        
        try:
            vehicle = Vehicle.objects.filter(status="active", auction_end_date__gte=timezone.now())
            vehicles = vehicle.order_by("-auction_start_date")
            if request.query_params.get("brand"):
                vehicles = vehicles.filter(model__brand__id=request.query_params.get("brand"))
            if request.query_params.get("model"):
                vehicles = vehicles.filter(model__id=request.query_params.get("model"))
            if request.query_params.get("year_range"):
                year_range = request.query_params.get("year_range").split("-")
                vehicles = vehicles.filter(year__gte=int(year_range[0]), year__lte=int(year_range[1]))
            serializer = VehicleSerializer(vehicles, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        
        
class VehicleView(APIView):
    
    def get(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
            serializer = VehicleDetailSerializer(vehicle, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)