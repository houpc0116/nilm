import paho.mqtt.client as mqtt
import datetime, time
import random, json


# MQTT SETTING
broker = '34.81.209.62'
port = 1883
topic = "ml"
Keep_Alive_Interval = 60
client_id = f'python-mqtt-{random.randint(0, 1000)}'

# 設置日期時間的格式
ISOTIMEFORMAT = '%m/%d %H:%M:%S'

# 初始化地端程式
mqttc = mqtt.Client(client_id)

# 設定登入帳號密碼
mqttc.username_pw_set(username="houpc16", password="awin_nilm")

mqttc.connect(broker, int(port), int(Keep_Alive_Interval))

#while True:
#t0 = random.randint(0,30)
fileName = 'GRU_iawe_clothes_iron' #檔案名稱, 修改這裡
t = now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
payload = {'dateTime':t, 'fileName':fileName}
print (json.dumps(payload))
# 要發布的主題和內容
mqttc.publish(topic, json.dumps(payload))
#time.sleep(1)