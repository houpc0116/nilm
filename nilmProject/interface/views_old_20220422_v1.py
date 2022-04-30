from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum
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

    
    # 計算本周第一天和最後一天
    currentDateTime = datetime.datetime.now()
    this_week_start = currentDateTime - timedelta(days=currentDateTime.weekday())
    this_week_end = now + timedelta(days=6-now.weekday())

    json_lists = []
    obj_item = Sensor.objects.filter(device=device).filter(datetime__range = [this_week_start, this_week_end]).order_by('-datetime')
    for post in obj_item:
        json_dict=model_to_dict(post)
        json_lists.append(json_dict)
    
    dataset = {'data':json_lists}
    return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')