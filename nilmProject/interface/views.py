from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum, Q
from interface.models import Sensor
import hashlib, json, re
from django.forms.models import model_to_dict
import datetime
from datetime import timedelta
# Create your views here.

def redirectWeb(request):
	return render(request, 'index_sensor.html')

def getSensortData(request):
    device = request.GET.get('device', -1)
    
    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    
    # 取得今天日期
    todate = datetime.date.today()

    json_lists = []
    if device == "elec110":
       # 電器 - 110 V
       # 聚合
       obj_item = Sensor.objects.filter(Q(device=device) | Q(device__contains='plug1')).filter(datetime__contains=todate).order_by('-datetime')
       for post in obj_item:
           json_dict=model_to_dict(post)
           json_lists.append(json_dict)

    else:
        # 電器 - 220 V
        # 聚合
        obj_item = Sensor.objects.filter(Q(device=device) | Q(device__contains='plug2')).filter(datetime__contains=todate).order_by('-datetime')
        for post in obj_item:
            json_dict=model_to_dict(post)
            json_lists.append(json_dict)

    dataset = {'data':json_lists}
    return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')