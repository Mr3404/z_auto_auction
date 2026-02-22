from rest_framework import serializers
from django.contrib.auth.models import User
from auction.models import VehicleBrand, VehicleModel, Vehicle, VehicleImage, VehicleVideo, Bid


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = "__all__"


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"


class VehicleModelSerializer(serializers.ModelSerializer):
    brand = VehicleBrandSerializer()
    class Meta:
        model = VehicleModel
        fields = ["id", "brand", "model"]


class UserVehicleSerializer(serializers.ModelSerializer):
    model = VehicleModelSerializer()
    image = serializers.SerializerMethodField()
    current_highest_bid = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ["id", "model", "year", "starting_price", "current_highest_bid", "auction_start_date", "auction_end_date", "image"]

    def get_image(self, obj):
        image = obj.vehicle_image.first()
        if image:
            return image.image.url
        return None
    
    def get_current_highest_bid(self, obj):
        highest_bid = obj.vehicle_bid.order_by('-amount').first()
        return highest_bid.amount if highest_bid and highest_bid.amount > obj.starting_price else obj.starting_price


class VehicleSerializer(serializers.ModelSerializer):
    model = VehicleModelSerializer()
    image = serializers.SerializerMethodField()
    current_highest_bid = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ["id", "model", "year", "current_highest_bid", "auction_start_date", "auction_end_date", "image"]

    def get_image(self, obj):
        image = obj.vehicle_image.first()
        if image:
            return image.image.url
        return None
    
    def get_current_highest_bid(self, obj):
        highest_bid = obj.vehicle_bid.order_by('-amount').first()
        return highest_bid.amount if highest_bid and highest_bid.amount > obj.starting_price else obj.starting_price
    
    

class VehicleDetailSerializer(serializers.ModelSerializer):
    model = VehicleModelSerializer()
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    current_highest_bid = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ["id", "model", "year", "vin", "kilometers", "engine_size", "transmission", "fuel_type","color", 
                "description", "status", "starting_price", "auction_start_date", "auction_end_date", "user", "images", "videos", "current_highest_bid"]
        
    def get_images(self, obj):
        return [img.image.url for img in obj.vehicle_image.all()]
        
    
    def get_videos(self, obj):
        return [video.video.url for video in obj.vehicle_video.all()]
    
    
    def get_current_highest_bid(self, obj):
        highest_bid = obj.vehicle_bid.order_by('-amount').first()
        return [highest_bid.amount if highest_bid else obj.starting_price]