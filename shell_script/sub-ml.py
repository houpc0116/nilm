## 放置在 Web Server
import paho.mqtt.client as mqtt
import datetime, time
import random, json
import os
import subprocess

#MQTT SETTING
broker = '34.81.209.62'
#broker = '206.189.154.58'
port = 1883
#topic = "sensor/engery"
#topic = "nilm"
topic = "ml"
Keep_Alive_Interval = 60
client_id = f'python-mqtt-{random.randint(0, 1000)}'
now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# Subscribe
def on_connect(client, userdata, flags, rc):
  mqttc.subscribe(topic, 0)

def on_message(mosq, obj, msg):
    m_decode = str(msg.payload.decode('utf-8', 'ignore'))
    #print("message received",m_decode)
    #print(type(m_decode))
    m_in=json.loads(m_decode)
    #print(type(m_in))
    fileName = m_in['fileName']
    output = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".png")
    output1 = subprocess.getoutput("wget -P /home/houpc16/djangoenv/nilmProject/static/analyze -N http://140.120.13.178:2020/"+fileName+".txt")
  

def on_subscribe(mosq, obj, mid, granted_qos):
  pass


#MAIN
mqttc = mqtt.Client(client_id)

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.username_pw_set(username="houpc16", password="awin_nilm")
# Connect
#mqttc.tls_set(ca_certs="ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
mqttc.connect(broker, int(port), int(Keep_Alive_Interval))

# Continue the network loop & close db-connection
mqttc.loop_forever()
