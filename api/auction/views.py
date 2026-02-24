from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
from auction.models import *
from .serializers import *


class AddBidView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        data = request.data
        data["bidder"] = request.user.id
        vehicle = Vehicle.objects.get(id=data.get("vehicle"))
        if vehicle.auction_end_date < timezone.now():
            return Response({"error": "Auction has ended"}, status.HTTP_400_BAD_REQUEST)
        if vehicle.status != "active":
            return Response({"error": "Vehicle is not active"}, status.HTTP_400_BAD_REQUEST)
        if vehicle.starting_price > data["amount"]:
            return Response({"error": "Bid must be higher than starting price"}, status.HTTP_400_BAD_REQUEST)
        highest_bid = vehicle.vehicle_bid.order_by('-amount').first()
        if highest_bid and data["amount"] <= highest_bid.amount:
            return Response({"error": "Bid must be higher than current highest bid"}, status.HTTP_400_BAD_REQUEST)
        vehicle.current_price = data["amount"]
        vehicle.save()
        serializer = AddBidSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class BidListView(APIView):
    
    def get(self, request):
        try:
            bids = Bid.objects.all()
            serializer = BidSerializer(bids, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)


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
            if request.query_params.get("price"):
                if request.query_params.get("price") == "from_low":
                    vehicles = vehicles.order_by("current_price")
                elif request.query_params.get("price") == "from_high":
                    vehicles = vehicles.order_by("-current_price")
            serializer = VehicleSerializer(vehicles, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        
        
class VehicleView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk)
            serializer = VehicleDetailSerializer(vehicle, many=False)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        data = request.data
        serializer = AddVehicleSerializer(data=data, many=False)
        if serializer.is_valid():
            serializer.save(user=request.user)
            image = request.FILES.getlist("photo")
            if image:
                for img in image:
                    VehicleImage.objects.create(vehicle_id=serializer.data["id"], image=img)
            video = request.FILES.get("video")
            if video:
                VehicleVideo.objects.create(vehicle_id=serializer.data["id"], video=video) 
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        try:
            vehicle = Vehicle.objects.get(id=pk, user=request.user)
        except:
            return Response(status.HTTP_404_NOT_FOUND)
        data = request.data        
        serializer = AddVehicleSerializer(vehicle, data=data, partial=True, many=False)
        if serializer.is_valid():
            serializer.save()
            image = request.FILES.getlist("photo")
            if image:
                VehicleImage.objects.filter(vehicle_id=pk).delete()
                for img in image:
                    VehicleImage.objects.create(vehicle_id=pk, image=img)
            video = request.FILES.get("video")
            if video:
                VehicleVideo.objects.filter(vehicle_id=pk).delete()
                VehicleVideo.objects.create(vehicle_id=pk, video=video)
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)