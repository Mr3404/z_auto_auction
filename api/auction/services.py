from auction.models import *

def getVehicleByPriceRange(vehicle, min_price, max_price):
    bidded_vehicles = Bid.objects.filter(vehicle__in=vehicle)
    vehicles = Vehicle.objects.filter(id__in=Subquery(bidded_vehicles.values("vehicle_id").annotate(max_bid=Max("amount")).filter(max_bid__gte=min_price, max_bid__lte=max_price).values("vehicle_id")))
    print(vehicles)
    return None