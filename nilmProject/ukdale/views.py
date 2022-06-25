from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.db.models import Sum
from ukdale.models import Ukdale
import hashlib, json, re
from django.forms.models import model_to_dict
# Create your views here.

##正式
def showInfo1(request):
    house_id = request.GET.get('houseId', -1)
    post_list = Ukdale.objects.filter(house=house_id).values('device').distinct() #類別
    device = []
    
    for item in post_list:
      if re.match(r'aggregate', item['device'], re.I):
         d = []
         data = Ukdale.objects.filter(house=house_id).filter(device=item['device']).order_by('-datetime')[:1].values()
         result = Ukdale.objects.filter(house=house_id).filter(device=item['device']).aggregate(Sum("pw"))
         May = Ukdale.objects.filter(house=house_id).filter(device=item['device']).filter(datetime__range = ["2013-05-01", "2013-05-31"]).aggregate(Sum("pw"))                            
         Jun = Ukdale.objects.filter(house=house_id).filter(device=item['device']).filter(datetime__range = ["2013-06-01", "2013-06-30"]).aggregate(Sum("pw"))                            
         July = Ukdale.objects.filter(house=house_id).filter(device=item['device']).filter(datetime__range = ["2013-07-01", "2013-07-31"]).aggregate(Sum("pw"))
         Aug = Ukdale.objects.filter(house=house_id).filter(device=item['device']).filter(datetime__range = ["2013-08-01", "2013-08-31"]).aggregate(Sum("pw"))

         listCount = [May, Jun, July, Aug]
         for i in range(0, 4):
             objectsItem = {'device':item['device'], 'month':(i+5), 'val':listCount[i]}
             d.append(objectsItem)

         item = {'device':item['device'], 'obj':data, 'sum':result, 'val':d}
         device.append(item)
   
    return render(request, 'index_ukdale.html', {'category_list': device})

def getChartDataJson1(request, num=1):
#    if request.method == 'POST':
      post_list = Ukdale.objects.filter(house=num).values('device').distinct() #類別
      json_lists = []
      json_lists1 = []
      for item in post_list:
          if re.match(r'AGGREGATE_1', item['device'], re.I):
              obj_item = Ukdale.objects.filter(house=num).filter(device=item['device']).order_by('-datetime')[:60]
              for post in obj_item:
                  json_dict=model_to_dict(post)
                  json_lists.append(json_dict)
          else:
              obj_item = Ukdale.objects.filter(house=num).filter(device=item['device']).order_by('-datetime')[:20]
              for post in obj_item:
                  json_dict=model_to_dict(post)
                  json_lists1.append(json_dict)   
              #post = postToDictionary(obj_item)     
#      print(json_lists)
      dataset = {'data':json_lists, 'data1':json_lists1}
      return JsonResponse(dataset)
#      return HttpResponse(json.dumps(dataset, default=myconverter), content_type='application/json')