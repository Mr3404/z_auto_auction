from django.contrib import admin
from .models import *


@admin.register(VehicleBrand)
class VehicleBrandAdmin(admin.ModelAdmin):
    list_display = ["brand",]


@admin.register(VehicleModel)
class VehicleModelAdmin(admin.ModelAdmin):
    list_display = ["model"]


class VehicleImageAdminInlines(admin.TabularInline):
    model = VehicleImage
    extra = 0


class VehicleVideoAdminInlines(admin.TabularInline):
    model = VehicleVideo
    extra = 0


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    inlines = [
        VehicleImageAdminInlines, VehicleVideoAdminInlines
    ]
    list_display = ["vin", "year"]

