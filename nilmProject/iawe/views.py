from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum
from iawe.models import IAWE
import hashlib, json, re
from django.forms.models import model_to_dict
import datetime
# Create your views here.
def showInfo2(request):
    #device = request.GET.get('device', -1)
    post_list = IAWE.objects.values('device').distinct() #類別

    device = []
    for item in post_list:
        if re.match(r'MAINS', item['device'], re.I):
           data = IAWE.objects.filter(device=item['device']).order_by('-datetime')[:1].values()
           result = IAWE.objects.filter(device=item['device']).aggregate(Sum("active"))
           May = IAWE.objects.filter(device=item['device']).filter(datetime__range = ["2013-05-01", "2013-05-31"]).aggregate(Sum("active"))
           Jun = IAWE.objects.filter(device=item['device']).filter(datetime__range = ["2013-06-01", "2013-06-30"]).aggregate(Sum("active"))
           July = IAWE.objects.filter(device=item['device']).filter(datetime__range = ["2013-07-01", "2013-07-31"]).aggregate(Sum("active"))
           Aug = IAWE.objects.filter(device=item['device']).filter(datetime__range = ["2013-07-01", "2013-07-31"]).aggregate(Sum("active"))
           item = {'device':item['device'], 'obj':data, 'sum':result, 'may':May, 'jun':July, 'july':July, 'aug':Aug}
           device.append(item)

    return render(request, 'index_iawe.html', {'category_list': device})

def getChartDataJson2(request):
    device = request.GET.get('device', -1)

    def myconverter(o):
        if isinstance(o, datetime.datetime):
            return o.__str__()

    post_list = IAWE.objects.values('device').distinct() #類別
    json_lists = []
    json_lists1 = []
    for item in post_list:
        if re.match(r'MAINS', item['device'], re.I):
            obj_item = IAWE.objects.filter(device__contains=item['device']).order_by('-datetime')[:20]
            for post in obj_item:
               json_dict=model_to_dict(post)
               json_lists.append(json_dict)
        else:
            obj_item = IAWE.objects.filter(device=item['device']).order_by('-datetime')[:20]
            for post in obj_item:
                json_dict=model_to_dict(post)
                json_lists1.append(json_dict)


    dataset = {'data':json_lists, 'data1':json_lists1}
    return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')

