from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum
from nilm.models import Redd
import hashlib, json, re
from django.forms.models import model_to_dict
import datetime
# Create your views here.
def showInfo(request):
    house_id = request.GET.get('houseId', -1)
    post_list = Redd.objects.filter(house=house_id).values('device').distinct() #類別
    
    device = []
    for item in post_list:
        if re.match(r'MAINS', item['device'], re.I):
               data = Redd.objects.filter(house=house_id).filter(device=item['device']).order_by('-datetime')[:1].values()
               result = Redd.objects.filter(house=house_id).filter(device=item['device']).aggregate(Sum("pw"))
               April = Redd.objects.filter(house=house_id).filter(device=item['device']).filter(datetime__range = ["2011-04-01", "2011-04-30"]).aggregate(Sum("pw")) ##datetime 是欄位
               May = Redd.objects.filter(house=house_id).filter(device=item['device']).filter(datetime__range = ["2011-05-01", "2011-05-31"]).aggregate(Sum("pw"))               
               item = {'device':item['device'], 'obj':data, 'sum':result, 'april':April, 'may':May}
               device.append(item)
    #device_data = ["菜鸟教程1","菜鸟教程2","菜鸟教程3"]
    #views_dict = {"category":post_list, "data":device}
    return render(request, 'index.html', {'category_list': device})

##顯示圖表
def getChartData(request, num=1):
    post_list = Redd.objects.filter(house=num).values('device').distinct() #類別

    dataset = []
    for item in post_list:
        if re.match(r'MAINS', item['device'], re.I):
                data = serializers.serialize('json', Redd.objects.filter(house=num).filter(device=item['device']).order_by('-datetime')[:20])
                dataset.append(data)

    return HttpResponse(dataset)  # or JsonResponse({'data': data})

def getChartDataJson(request, num=1):
#    if request.method == 'POST':
#       dict_obj = [{"brand": "Ford", "model": "Mustang", "year": 1964}, {"brand": "Ford", "model": "Mustang", "year": num}]
#       obj_item = Redd.objects.filter(house=num).filter(device=item['device']).order_by('-datetime')[:20].values()
       ## datetime serial error
        def myconverter(o):
            if isinstance(o, datetime.datetime):
                return o.__str__()

        post_list = Redd.objects.filter(house=num).values('device').distinct() #類別
        json_lists = []
        json_lists1 = []
        for item in post_list:
           if re.match(r'MAINS', item['device'], re.I):
              obj_item = Redd.objects.filter(device__contains=item['device']).order_by('-datetime')[:20]
              for post in obj_item:
                  json_dict=model_to_dict(post)
                  json_lists.append(json_dict)

           else:
              obj_item = Redd.objects.filter(house=num).filter(device=item['device']).order_by('-datetime')[:1]
              for post in obj_item:
                  json_dict=model_to_dict(post)
                  json_lists1.append(json_dict)       
       
        dataset = {'data':json_lists, 'data1':json_lists1}
        return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')

