from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from auction.models import *
from .serializers import *


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
            vehicles = Vehicle.objects.all()
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