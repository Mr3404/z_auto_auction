from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import ForeignKeyWidget
from import_export.formats.base_formats import XLSX, CSV
from .models import *


class VehicleBrandResource(resources.ModelResource):
    class Meta:
        model = VehicleBrand
        fields = ('id', 'brand')
        import_id_fields = ('brand',) 


@admin.register(VehicleBrand)
class VehicleBrandAdmin(ImportExportModelAdmin):
    list_display = ["brand",]
    resource_class = VehicleBrandResource
    formats = [XLSX, CSV]


class VehicleModelResource(resources.ModelResource):
    brand = fields.Field(column_name='brand', attribute='brand', widget=ForeignKeyWidget(VehicleBrand, 'brand'))
    class Meta:
        model = VehicleModel
        fields = ('id', 'model', 'brand')
        import_id_fields = ('model',)
        
        
@admin.register(VehicleModel)
class VehicleModelAdmin(ImportExportModelAdmin):
    list_display = ["model", "brand"]
    resource_class = VehicleModelResource
    formats = [XLSX, CSV]


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
    list_display = ["vin", "year", "auction_start_date","status"]
    list_editable = ["auction_start_date", "status"]
    
    
@admin.register(Bid)
class VehicleBidAdmin(admin.ModelAdmin):
    list_display = ["amount"]
    