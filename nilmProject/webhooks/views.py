from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.forms.models import model_to_dict
import subprocess
import hashlib, json, re
# Create your views here.

def showMLResult(request, fileName):
    #fileName = 'GRU_iawe_clothes_iron'
    output = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".png >/dev/null 2>&1")
    output1 = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".txt >/dev/null 2>&1")

    message = {'response':'ok'}
    return JsonResponse(message)