#from django.shortcuts import render
from status.models import Status
from status.serializers import StatusSerializer

# Create your views here.
from rest_framework import viewsets


# Create your views here.
class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
