from django.db import models
from django.contrib.auth.models import User


class VehicleBrand(models.Model):
    brand = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Vehicle Brands"

    def __str__(self):
        return self.brand
    

class VehicleModel(models.Model):
    brand = models.ForeignKey(VehicleBrand, on_delete=models.CASCADE, related_name="vehicle_brand")
    model = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "Vehicle Model"

    def __str__(self):
        return self.model


class Vehicle(models.Model):
    TRANSMISSION_CHOICES = [
        ("manual", "Manual"),
        ("automatic", "Automatic"),
    ]

    FUEL_CHOICES = [
        ("petrol", "Petrol"),
        ("diesel", "Diesel"),
        ("electric", "Electric"),
        ("hybrid", "Hybrid") 
    ]
    
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("active", "Active"),
        ("sold", "Sold")
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vehicle_user")
    model = models.ForeignKey(VehicleModel, on_delete=models.CASCADE, related_name="vehicle_model")
    year = models.IntegerField(default=2000)
    vin = models.CharField(max_length=100, unique=True)
    kilometers = models.PositiveIntegerField()
    engine_size = models.CharField(max_length=20)
    transmission = models.CharField(choices=TRANSMISSION_CHOICES, max_length=50)
    fuel_type = models.CharField(choices=FUEL_CHOICES, max_length=50)
    color = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(choices=STATUS_CHOICES, default="pending", max_length=50)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    auction_start_date = models.DateTimeField(auto_now_add=False)
    auction_end_date = models.DateTimeField(auto_now_add=False)
    

    class Meta:
        verbose_name_plural = "Vehicles"

    def __str__(self):
        return self.model.model
    

class VehicleImage(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle_image")
    image = models.ImageField(upload_to="vehicle_images/")


class VehicleVideo(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle_video")
    video = models.FileField(upload_to="vehicle_videos/")


class Bid(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle_bid")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidded_user")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        verbose_name_plural = "Vehicle Bids"
    
    def __str__(self):
        return self.vehicle.model.model