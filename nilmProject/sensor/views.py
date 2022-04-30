from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from sensor.models import Sensor
from sensor.serializers import SensorSerializer

# Create your views here.
from rest_framework import generics

class SensorViewSet(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['device']