import paho.mqtt.client as mqtt
import datetime, time
import random, json
import mysql.connector
from mysql.connector import Error

# 連接 MySQL/MariaDB 資料庫
connection = mysql.connector.connect(
        host='35.201.210.50',          # 主機名稱
#        host='10.10.34.188',          # 主機名稱
#        host='192.168.101.19',          # 主機名稱
        database='nilm', # 資料庫名稱
        user='awin',        # 帳號
        password='awin')  # 密碼
cursor = connection.cursor()

#MQTT SETTING
broker = '127.0.0.1'
#broker = '206.189.154.58'
port = 1883
#topic = "sensor/engery"
#topic = "nilm"
topic = "plug3-1"
Keep_Alive_Interval = 60
client_id = f'python-mqtt-{random.randint(0, 1000)}'
now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

# Subscribe
def on_connect(client, userdata, flags, rc):
  mqttc.subscribe(topic, 0)

def on_message(mosq, obj, msg):
    m_decode = str(msg.payload.decode('utf-8', 'ignore'))
    print("message received",m_decode)
    print(type(m_decode) )
#    payload = m_decode.split('=')
#    print(payload[0])  TOPIC
#    m_in=json.loads(payload[1])
    m_in=json.loads(m_decode)
    print(type(m_in))
#    print(type(m_in['payload']) )
#    print(m_in['payload']['v'])
#    json_type = json.dumps(json_string)  #json.dumps(json1)
#    json_object = json.loads(json.dumps(json_string))
#    pairs = json_object.items()
#    print(pairs)

    dt_string = datetime.datetime.now()
    device = topic
#    device = 'airacondition'
#    print(m_in['v'] )
    # 新增資料
    sql = 'INSERT INTO sensor (datetime, device, vo, cu, active, reactive, apparent, pf, freq) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);'
    new_data = (dt_string, device, 0, 0, m_in['active_power'], 0, 0, m_in['pf'], 0)
    
#    cursor.execute(sql, new_data)
    try:
      cursor.execute(sql, new_data)
    except Error as e:
      print("Error: {}".format(e))

    # 確認資料有存入資料庫
    connection.commit()

#     message = msg.payload.decode('utf-8')
#     convertStr = json.dumps(message)
#     convertDict = json.loads(convertStr)
#     print(type(convertDict))
  

def on_subscribe(mosq, obj, mid, granted_qos):
  pass


#MAIN
mqttc = mqtt.Client(client_id)

# Assign event callbacks
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

mqttc.username_pw_set(username="aicap", password="0422331888")
# Connect
#mqttc.tls_set(ca_certs="ca.crt", tls_version=ssl.PROTOCOL_TLSv1_2)
mqttc.connect(broker, int(port), int(Keep_Alive_Interval))

# Continue the network loop & close db-connection
mqttc.loop_forever()
connection.close()
