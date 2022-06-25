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

    
    # 取得今天日期
    todate = datetime.date.today()
    
    json_lists = []
    # 聚合
    #obj_item = Sensor.objects.filter(device__contains=device).order_by('-datetime')[:20]
    obj_item = Sensor.objects.filter(device=device).filter(datetime__contains=todate).order_by('-datetime')
    for post in obj_item:
        json_dict=model_to_dict(post)
        json_lists.append(json_dict)


    json1_lists = []
    json2_lists = []
    if device == "elec110":
       # 電器 - 110 V
       post_list = Sensor.objects.filter(device__contains='plug1').values('device').distinct() #類別
       for item in post_list:
           if re.match(r'plug1-1', item['device'], re.I):
              obj_item = Sensor.objects.filter(device=item['device']).filter(datetime__contains=todate).order_by('-datetime')
              for post in obj_item:
                  json_dict=model_to_dict(post)
                  json1_lists.append(json_dict)

           elif re.match(r'plug1-2', item['device'], re.I):
              obj_item = Sensor.objects.filter(device=item['device']).filter(datetime__contains=todate).order_by('-datetime')
              for post in obj_item:
                  json_dict=model_to_dict(post)
                  json2_lists.append(json_dict)
    else:
        # 電器 - 220 V
        post_list = Sensor.objects.filter(device__contains='plug2').values('device').distinct() #類別
        for item in post_list:
            if re.match(r'plug2-1', item['device'], re.I):
               obj_item = Sensor.objects.filter(device=item['device']).filter(datetime__contains=todate).order_by('-datetime')
               for post in obj_item:
                   json_dict=model_to_dict(post)
                   json1_lists.append(json_dict)

            elif re.match(r'plug2-2', item['device'], re.I):
               obj_item = Sensor.objects.filter(device=item['device']).filter(datetime__contains=todate).order_by('-datetime')
               for post in obj_item:
                   json_dict=model_to_dict(post)
                   json2_lists.append(json_dict)
    

    dataset = {'data':json_lists, 'data1':json1_lists, 'data2':json2_lists}
    return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')