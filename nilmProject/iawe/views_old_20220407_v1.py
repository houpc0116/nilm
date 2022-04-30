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
    device = request.GET.get('device', -1)

    data = IAWE.objects.filter(device=device).order_by('-datetime')[:1].values()
#    data = list(IAWE.objects.filter(device=device).order_by('-id')[:1].values())
    result = IAWE.objects.filter(device=device).aggregate(Sum("active"))
    May = IAWE.objects.filter(device=device).filter(datetime__range = ["2013-05-01", "2013-05-31"]).aggregate(Sum("active")) 
    June = IAWE.objects.filter(device=device).filter(datetime__range = ["2013-06-01", "2013-06-30"]).aggregate(Sum("active"))
    July = IAWE.objects.filter(device=device).filter(datetime__range = ["2013-07-01", "2013-07-31"]).aggregate(Sum("active"))
    Aug = IAWE.objects.filter(device=device).filter(datetime__range = ["2013-08-01", "2013-08-31"]).aggregate(Sum("active"))               
    item = {'device':device, 'obj':data, 'sum':result, 'may':May, 'june':June, 'July':July, 'Aug':Aug}
    #device_data = ["菜鸟教程1","菜鸟教程2","菜鸟教程3"]
    #views_dict = {"category":post_list, "data":device}
    return render(request, 'index_iawe.html', {'category_list': item})
