from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from banner.models import Banner
from .serializers import BannerSerializer


class BannerView(APIView):
    
    def get(self, request):
        try:
            banners = Banner.objects.filter(is_active=True)
            serializer = BannerSerializer(banners, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        except:
            return Response(status.HTTP_404_NOT_FOUND)