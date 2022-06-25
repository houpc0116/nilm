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
    this_week_end = currentDateTime + timedelta(days=6-currentDateTime.weekday())
    # 取得這星期的日期
    week_date = []
    for i in range(0, 7):
        this_week_date = this_week_start + datetime.timedelta(days=i)
        week_date.append(this_week_date.strftime('%Y-%m-%d'))

    json_lists = []
    obj_item = Sensor.objects.filter(device=device).filter(datetime__range = [this_week_start.strftime('%Y-%m-%d'), this_week_end.strftime('%Y-%m-%d')]).order_by('-datetime')
    for post in obj_item:
        json_dict=model_to_dict(post)
        json_lists.append(json_dict)
    
    dataset = {'data':json_lists, 'week_date':week_date}
    return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')