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

            
            if dataset == 'iawe' and algorithm == 'gru' and appliances == 'clothes_iron':
                output = subprocess.getoutput("python /home/houpc16/GRU/GRU_iawe_clothes_iron.py > /home/houpc16/GRU/result.txt")
                #讀取檔案
                f = open('/home/houpc16/GRU/result.txt')
                for line in f:
                    if line.find('Recall') != -1:
                        recall = line
                    elif line.find('Accuracy') != -1:
                        accuracy = line
                    elif line.find('F1 Score') != -1:
                        f1score = line
                    elif line.find('Precision') != -1:
                        precision = line
                    elif line.find('Relative error in total energy') != -1:
                        relativerror = line
                    elif line.find('Mean absolute error') != -1:
                        meanabsoluterror = line


                result = {'status':'ok', 'image':'GRU_iawe_clothes_iron', 'recall':recall, 'accuracy':accuracy, 'f1score':f1score, 'precision':precision, 'relativerror':relativerror, 'meanabsoluterror':meanabsoluterror}
                return HttpResponse(json.dumps(result))
                #f = open('/Users/hou/Sites/djangogirls/shell_script/result.txt')
            elif dataset == 'iawe' and algorithm == 'gru' and appliances == 'fridge':
                output = subprocess.getoutput("python /home/houpc16/GRU/GRU_iawe_fridge.py > /home/houpc16/GRU/result.txt")
                #讀取檔案
                f = open('/home/houpc16/GRU/result.txt')
                for line in f:
                    if line.find('Recall') != -1:
                        recall = line
                    elif line.find('Accuracy') != -1:
                        accuracy = line
                    elif line.find('F1 Score') != -1:
                        f1score = line
                    elif line.find('Precision') != -1:
                        precision = line
                    elif line.find('Relative error in total energy') != -1:
                        relativerror = line
                    elif line.find('Mean absolute error') != -1:
                        meanabsoluterror = line


                result = {'status':'ok', 'image':'GRU_iawe_fridge', 'recall':recall, 'accuracy':accuracy, 'f1score':f1score, 'precision':precision, 'relativerror':relativerror, 'meanabsoluterror':meanabsoluterror}
                return HttpResponse(json.dumps(result))
            elif dataset == 'iawe' and algorithm == 'gru' and appliances == 'wash_dryer':
                output = subprocess.getoutput("python /home/houpc16/GRU/GRU_iawe_washing_machine.py > /home/houpc16/GRU/result.txt")
                #讀取檔案
                f = open('/home/houpc16/GRU/result.txt')
                for line in f:
                    if line.find('Recall') != -1:
                        recall = line
                    elif line.find('Accuracy') != -1:
                        accuracy = line
                    elif line.find('F1 Score') != -1:
                        f1score = line
                    elif line.find('Precision') != -1:
                        precision = line
                    elif line.find('Relative error in total energy') != -1:
                        relativerror = line
                    elif line.find('Mean absolute error') != -1:
                        meanabsoluterror = line


                result = {'status':'ok', 'image':'GRU_iawe_washing_machine', 'recall':recall, 'accuracy':accuracy, 'f1score':f1score, 'precision':precision, 'relativerror':relativerror, 'meanabsoluterror':meanabsoluterror}
                return HttpResponse(json.dumps(result))
