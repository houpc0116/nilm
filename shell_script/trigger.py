import datetime, time
import os.path
import requests
## 紀錄連線狀態
def checkStatus(status):
    fp = open('rd.txt', 'w')
    fp.write(status)
    fp.close()

## trigger Line Notify
def triggerLine(type):
    dt_string = datetime.datetime.now()
    if type == 'offline':
       msg = str(dt_string)+'\n網路斷線'
    else:
       msg = str(dt_string)+'\n恢復連線'
    
    url = 'https://script.google.com/macros/s/AKfycbyh6I88tMe8pEbDwPmzwmIpz0WSgQm5Kvo540DrL9ki3S20jzyBTGPCnxZnub0BGCIZ/exec'
    myobj = {'msg': msg} 
   
    x = requests.post(url, data = myobj)

## trigger DataBase
def triggerLog(type):
    if type == 'offline':
       msg_log = '網路斷線'
    else:
       msg_log = '恢復連線'

    dt_string = datetime.datetime.now()
    url = 'http://35.221.191.175:8088/api/status/'
    headers = {"Content-Type": "application/json; charset=utf-8"}
    payload = {'datetime':str(dt_string), 'content': msg_log}
    response = requests.post(url, headers=headers, json=payload)

## 主程式
f = open('connect.txt', 'r')
#print(f.read())
connect = f.read()
f.close()

## 現在連線時間
now_dt = round(time.time())
#print(connect)
if os.path.exists('rd.txt') == True:
   ## 已連線
   f = open('rd.txt', 'r')
   #print(f.read())
   status = f.read()
   f.close()
   
   if (now_dt - int(connect)) > 60:
       print('offline')
       ## 紀錄斷線
       checkStatus('offline')
       triggerLine('offline')
       triggerLog('offline')
   elif status == 'offline':
       print('online')
       ## 紀錄連線
       checkStatus('online')
       triggerLine('online')
       triggerLog('online')

else:
   ## 初始連線
   checkStatus('online')
