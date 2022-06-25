from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse

from keras.models import load_model as keras_load_model
import numpy as np
import os
import subprocess
import hashlib, json, re
# Create your views here.
def redirectionPage(request):
    return render(request, 'analyze.html')


def showResult(request):
    if request.method == "POST":
            dataset = request.POST.get("dataset", None)
            algorithm = request.POST.get("algorithm", None)
            appliances = request.POST.get("appliances", None)

            #output = subprocess.getoutput("python /home/houpc16/GRU/GRU_iawe_clothes_iron.py > /home/houpc16/GRU/result.txt")
            fileName = "RNN_iawe_clothes_iron"
            output = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".png >/dev/null 2>&1")
            output1 = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".txt >/dev/null 2>&1")

            #讀取檔案
            f = open('/home/houpc16/djangoenv/nilmProject/static/analyze/'+fileName+'.txt')
            #content = f.read()
            for line in f:
                content = line
            #f.close

            result = {'status':'ok', 'image':fileName, 'content':content}
            return HttpResponse(json.dumps(result))
            #f = open('/Users/hou/Sites/djangogirls/shell_script/result.txt')

