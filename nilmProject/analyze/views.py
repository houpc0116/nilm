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
            #GRU
            if dataset == 'iawe' and algorithm == 'gru' and appliances == 'clothes_iron':
                 #output = subprocess.getoutput("python /home/houpc16/GRU/GRU_iawe_clothes_iron.py > /home/houpc16/GRU/result.txt")
                 fileName = "GRU_iawe_clothes_iron"

            elif dataset == 'iawe' and algorithm == 'gru' and appliances == 'fridge':
                 fileName = "GRU_iawe_fridge"

            elif dataset == 'iawe' and algorithm == 'gru' and appliances == 'wash_dryer':
                 fileName = "GRU_iawe_washing_machine"

            elif dataset == 'redd' and algorithm == 'gru' and appliances == 'fridge':
                 fileName = "GRU_redd_fridge"

            elif dataset == 'redd' and algorithm == 'gru' and appliances == 'microwave':
                 fileName = "GRU_redd_microwave"

            elif dataset == 'redd' and algorithm == 'gru' and appliances == 'sockets':
                 fileName = "GRU_redd_sockets"

            elif dataset == 'ukdale' and algorithm == 'gru' and appliances == 'kettle':
                 fileName = "GRU_ukdale_kettle"
            
            elif dataset == 'ukdale' and algorithm == 'gru' and appliances == 'microwave':
                 fileName = "GRU_ukdale_microwave"

            elif dataset == 'ukdale' and algorithm == 'gru' and appliances == 'wash_dryer':
                 fileName = "GRU_ukdale_washer_dryer"

            elif dataset == 'sensor' and algorithm == 'gru' and appliances == 'notebook':
                 fileName = "GRU_elec110V_plug1"

            elif dataset == 'sensor' and algorithm == 'gru' and appliances == 'air':
                 fileName = "GRU_elec110V_plug2"
            #RNN
            elif dataset == 'iawe' and algorithm == 'rnn' and appliances == 'clothes_iron':
                 fileName = "RNN_iawe_clothes_iron"

            elif dataset == 'iawe' and algorithm == 'rnn' and appliances == 'fridge':
                 fileName = "RNN_iawe_fridge"

            elif dataset == 'iawe' and algorithm == 'rnn' and appliances == 'wash_dryer':
                 fileName = "RNN_iawe_washing_machine"

            elif dataset == 'redd' and algorithm == 'rnn' and appliances == 'fridge':
                 fileName = "RNN_redd_fridge"

            elif dataset == 'redd' and algorithm == 'rnn' and appliances == 'microwave':
                 fileName = "RNN_redd_microwave"

            elif dataset == 'redd' and algorithm == 'rnn' and appliances == 'sockets':
                 fileName = "RNN_redd_sockets"

            elif dataset == 'ukdale' and algorithm == 'rnn' and appliances == 'kettle':
                 fileName = "RNN_ukdale_kettle"
            
            elif dataset == 'ukdale' and algorithm == 'rnn' and appliances == 'microwave':
                 fileName = "RNN_ukdale_microwave"

            elif dataset == 'ukdale' and algorithm == 'rnn' and appliances == 'wash_dryer':
                 fileName = "RNN_ukdale_washer_dryer"

            elif dataset == 'sensor' and algorithm == 'rnn' and appliances == 'notebook':
                 fileName = "RNN_elec110V_plug1"

            elif dataset == 'sensor' and algorithm == 'rnn' and appliances == 'air':
                 fileName = "RNN_elec110V_plug2"
            #DAE
            elif dataset == 'iawe' and algorithm == 'dae' and appliances == 'clothes_iron':
                 fileName = "DAE_iawe_clothes_iron"

            elif dataset == 'iawe' and algorithm == 'dae' and appliances == 'fridge':
                 fileName = "DAE_iawe_fridge"

            elif dataset == 'iawe' and algorithm == 'dae' and appliances == 'wash_dryer':
                 fileName = "DAE_iawe_washer_dryer"

            elif dataset == 'redd' and algorithm == 'dae' and appliances == 'fridge':
                 fileName = "DAE_redd_fridge"

            elif dataset == 'redd' and algorithm == 'dae' and appliances == 'microwave':
                 fileName = "DAE_redd_microwave"

            elif dataset == 'redd' and algorithm == 'dae' and appliances == 'sockets':
                 fileName = "DAE_redd_sockets"

            elif dataset == 'ukdale' and algorithm == 'dae' and appliances == 'kettle':
                 fileName = "DAE_ukdale_kettle"
            
            elif dataset == 'ukdale' and algorithm == 'dae' and appliances == 'microwave':
                 fileName = "DAE_ukdale_microwave"

            elif dataset == 'ukdale' and algorithm == 'dae' and appliances == 'wash_dryer':
                 fileName = "DAE_ukdale_washer_dryer"

            elif dataset == 'sensor' and algorithm == 'dae' and appliances == 'notebook':
                 fileName = "DAE_elec110V_plug1"

            elif dataset == 'sensor' and algorithm == 'dae' and appliances == 'air':
                 fileName = "DAE_elec110V_plug2"
            #Window-GRU
            elif dataset == 'iawe' and algorithm == 'wingru' and appliances == 'clothes_iron':
                 fileName = "Window-GRU_iawe_clothes_iron"

            elif dataset == 'iawe' and algorithm == 'wingru' and appliances == 'fridge':
                 fileName = "Window-GRU_iawe_fridge"

            elif dataset == 'iawe' and algorithm == 'wingru' and appliances == 'wash_dryer':
                 fileName = "Window-GRU_iawe_washer_machine"

            elif dataset == 'redd' and algorithm == 'wingru' and appliances == 'fridge':
                 fileName = "Window-GRU_redd_fridge"

            elif dataset == 'redd' and algorithm == 'wingru' and appliances == 'microwave':
                 fileName = "Window-GRU_redd_microwave"

            elif dataset == 'redd' and algorithm == 'wingru' and appliances == 'sockets':
                 fileName = "Window-GRU_redd_sockets"

            elif dataset == 'ukdale' and algorithm == 'wingru' and appliances == 'kettle':
                 fileName = "Window-GRU_ukdale_kettle"
            
            elif dataset == 'ukdale' and algorithm == 'wingru' and appliances == 'microwave':
                 fileName = "Window-GRU_ukdale_microwave"

            elif dataset == 'ukdale' and algorithm == 'wingru' and appliances == 'wash_dryer':
                 fileName = "Window-GRU_ukdale_washer_dryer"

            elif dataset == 'sensor' and algorithm == 'wingru' and appliances == 'notebook':
                 fileName = "Window-GRU_elec110V_plug1"

            elif dataset == 'sensor' and algorithm == 'wingru' and appliances == 'air':
                 fileName = "Window-GRU_elec110V_plug2"
            #ShortSeq2Point
            elif dataset == 'iawe' and algorithm == 'seq2' and appliances == 'clothes_iron':
                 fileName = "Seq2_iawe_clothes_iron"

            elif dataset == 'iawe' and algorithm == 'seq2' and appliances == 'fridge':
                 fileName = "Seq2_iawe_fridge"

            elif dataset == 'iawe' and algorithm == 'seq2' and appliances == 'wash_dryer':
                 fileName = "Seq2_iawe_washer_dryer"

            elif dataset == 'redd' and algorithm == 'seq2' and appliances == 'fridge':
                 fileName = "Seq2_redd_fridge"

            elif dataset == 'redd' and algorithm == 'seq2' and appliances == 'microwave':
                 fileName = "Seq2_redd_microwave"

            elif dataset == 'redd' and algorithm == 'seq2' and appliances == 'sockets':
                 fileName = "Seq2_redd_sockets"

            elif dataset == 'ukdale' and algorithm == 'seq2' and appliances == 'kettle':
                 fileName = "Seq2_ukdale_kettle"
            
            elif dataset == 'ukdale' and algorithm == 'seq2' and appliances == 'microwave':
                 fileName = "Seq2_ukdale_microwave"

            elif dataset == 'ukdale' and algorithm == 'seq2' and appliances == 'wash_dryer':
                 fileName = "Seq2_ukdale_washer_dryer"
                 
            elif dataset == 'sensor' and algorithm == 'seq2' and appliances == 'notebook':
                 fileName = "Seq2_elec110V_plug1"

            elif dataset == 'sensor' and algorithm == 'seq2' and appliances == 'air':
                 fileName = "Seq2_elec110V_plug2"
            
            #output = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".png >/dev/null 2>&1")
            #output1 = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".txt >/dev/null 2>&1")

            #讀取檔案
            f = open('/home/houpc16/djangoenv/nilmProject/static/analyze/'+fileName+'.txt')
            #content = f.read()
            for line in f:
                content = line
            #f.close

            result = {'status':'ok', 'image':fileName, 'content':content}
            return HttpResponse(json.dumps(result))
            #f = open('/Users/hou/Sites/djangogirls/shell_script/result.txt')