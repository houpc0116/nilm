from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum
from sensor.models import Sensor
import hashlib, json, re
from django.forms.models import model_to_dict
import datetime

# Create your views here.
def getObjectInfo(request):
    device = request.GET.get('device', -1)

    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    json_lists = []
    obj_item = Sensor.objects.filter(device__contains=device)
    for post in obj_item:
        json_dict=model_to_dict(post)
        json_lists.append(json_dict)

    dataset = {'data':json_lists}
    return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')
