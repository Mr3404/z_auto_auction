from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

from ..auction.serializers import VehicleSerializer, BidSerializer, UserVehicleSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]
    
    
class UserProfileSerializer(serializers.ModelSerializer):
    my_vehicles = serializers.SerializerMethodField()
    my_bids = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "is_staff", "is_active", "my_vehicles", "my_bids"]
        
    def get_my_vehicles(self, obj):
        vehicles = obj.vehicle_user.all()
        return UserVehicleSerializer(vehicles, many=True).data
    
    def get_my_bids(self, obj):
        bids = obj.bidded_user.all()
        return BidSerializer(bids, many=True).data