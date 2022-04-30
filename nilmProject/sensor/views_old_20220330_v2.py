from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from sensor.models import Sensor
from sensor.serializers import SensorSerializer

# Create your views here.
from rest_framework import generics

class SensorViewSet(generics.ListAPIView):
    serializer_class = SensorSerializer

    def get_queryset(self):
    	queryset = Sensor.objects.all()
    	username = self.request.query_params.get('device')
        if username is not None:
            queryset = queryset.filter(device__username=username)
        return queryset