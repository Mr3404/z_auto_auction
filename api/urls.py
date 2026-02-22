from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .auth.views import *
from .auction.views import *


urlpatterns = [
    path('register/', ResgisterUserView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh-token/', TokenRefreshView.as_view()),
    path('user-profile/', UserProfileView.as_view()),

    path('vehicle-brands/', VehicleBrandView.as_view()),
    path('vehicle-models/', VehicleModelView.as_view()),
    path('vehicle-list/', VehicleListView.as_view()),
    path('vehicle/<int:pk>/', VehicleView.as_view()),
]