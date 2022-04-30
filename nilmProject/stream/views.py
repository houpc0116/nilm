from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.core import serializers
from django.utils.timezone import now
from django.forms.models import model_to_dict
# Create your views here.
from stream.models import Sensor
import hashlib, json, re
import time, datetime

def eventsource(request):
    response = StreamingHttpResponse(stream_generator(), content_type="text/event-stream")
    response['Cache-Control'] = 'no-cache'
    return response

def stream_generator():
    while True:
        # 发送事件数据
        # yield 'event: date\ndata: %s\n\n' % str(now())
        data = Sensor.objects.order_by('-datetime')[:1]
        dateTime = str(data[0].datetime)
        personDict = {
           'id': data[0].id,
           'device': data[0].device,
           'datetime': dateTime,
           'vo': data[0].vo,
           'cu': data[0].cu,
           'active': data[0].active,
           'reactive': data[0].reactive,
           'apparent': data[0].apparent,
           'pf': data[0].pf,
           'freq': data[0].freq,
        }

        #appDict = {'id':data[0].id, 'datetime':data[0].datatime}
        app_json = json.dumps(personDict)
        # 发送数据
        yield u'data: %s\n\n' % app_json
        time.sleep(3)