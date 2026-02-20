from rest_framework import serializers
from django.contrib.auth.models import User
from auction.models import VehicleBrand, VehicleModel, Vehicle, VehicleImage, VehicleVideo


class VehicleBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = VehicleBrand
        fields = "__all__"


class VehicleModelSerializer(serializers.ModelSerializer):
    brand = VehicleBrandSerializer()
    class Meta:
        model = VehicleModel
        fields = ["id", "brand", "model"]


class VehicleSerializer(serializers.ModelSerializer):
    model = VehicleModelSerializer()
    image = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ["id", "model", "year", "starting_price", "auction_start_date", "auction_end_date", "image"]

    def get_image(self, obj):
        image = obj.vehicle_image.first()
        if image:
            return image.image.url
        return None
    

class VehicleDetailSerializer(serializers.ModelSerializer):
    model = VehicleModelSerializer()
    images = serializers.SerializerMethodField()
    videos = serializers.SerializerMethodField()
    class Meta:
        model = Vehicle
        fields = ["id", "model", "year", "vin", "kilometers", "engine_size", "transmission", "fuel_type","color", 
                "description", "status", "starting_price", "auction_start_date", "auction_end_date", "user", "images", "videos"]
        
    def get_images(self, obj):
        return [img.image.url for img in obj.vehicle_image.all()]
        
    
    def get_videos(self, obj):
        return [video.video.url for video in obj.vehicle_video.all()]