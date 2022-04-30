import json
import requests
import datetime
import uuid
import traceback
from websocket import create_connection
# base和token會在cmd(命令提示元)，啟動jupyter notebook時出現
#notebook_path = '/hello_jupyter.ipynb'
notebook_path = '/GRU_iawe_clothes_iron.ipynb'
base = 'http://127.0.0.1:8888'
headers = {'Authorization': 'Token 24d195359df97e36ad9b663787dc046b56ac91a9b9bff7ef'}

url = base + '/api/sessions'
#print(url)
params = '{"path":\"%s\","type":"notebook","name":"","kernel":{"id":null,"name":"python3"}}' % notebook_path
response = requests.post(url, headers=headers, data=params)
session = json.loads(response.text)
kernel = session["kernel"]
#print(kernel)

# 讀取notebook檔案，並獲取每個Cell裡的Code
url = base + '/api/contents' + notebook_path
response = requests.get(url,headers=headers)
#print(response)
file = json.loads(response.text)
code = [ c['source'] for c in file['content']['cells'] if len(c['source'])>0 ]
#print(kernel["id"])
#print(code[0])

#簡單來說就是 Jupyter Notebook API 會依照你給的 Code，去處理並把結果 Response 回來
def send_execute_request(code):
    msg_type = 'execute_request';
    content = { 'code' : code, 'silent':False }
    hdr = { 'msg_id' : uuid.uuid1().hex, 
        'username': 'test', 
        'session': uuid.uuid1().hex, 
        'data': datetime.datetime.now().isoformat(),
        'msg_type': msg_type,
        'version' : '5.0' }
    msg = { 'header': hdr, 'parent_header': hdr, 
        'metadata': {},
        'content': content }
    return msg


# 開始啟動 WebSocket channels (request/reply)
ws = create_connection("ws://127.0.0.1:8888/api/kernels/"+kernel["id"]+"/channels?session_id"+session["id"], header=headers)
for c in code:
    ws.send(json.dumps(send_execute_request(c)))


# 我們只拿Code執行完的訊息結果，其他訊息將被忽略
for i in range(0, len(code)):
    try:
        msg_type = ''
        while True:
            rsp = json.loads(ws.recv())
            msg_type = rsp["msg_type"]
            #print(msg_type)
    # 顯示列印內容
            if msg_type == "stream":
                print(rsp["content"]["text"])
            elif msg_type == "execute_result":
                # 顯示圖片編碼
                if "image/png" in (rsp["content"]["data"].keys()):
                    print(rsp["content"]["data"]["image/png"])
                # 顯示輸出結果
                else:
                    print(rsp["content"]["data"]["text/plain"])
    # 顯示計算表格
            elif msg_type == "display_data":
                print(rsp["content"]["data"]["image/png"])
    # 顯示錯誤訊息
            elif msg_type == "error":
                print(rsp["content"]["traceback"])
    # 當狀態為idle，代表ws.recv()已經沒有任何訊息
            elif msg_type == "status" and rsp["content"]["execution_state"] == "idle":
                break 
    except:
        traceback.print_exc()
        ws.close()
            
ws.close()
