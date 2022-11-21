1. shell_script : MQTT sub/pub
   requests: 
   python3.8

2. nilmProject WebSite
   requests: 
   python3.7.12
   mysql 5
   django 3.2# nilm
   https://www.notion.so/Django-nginx-uwsgi-25a21a5b58d54d3a9b631dd6f6a46db7#8772ebab04284ba4ae2a12a34fcedefc

2022.05.22 新增pub.py
   -- 此段程式放在 ML Server 裡的Jupyter 最後一個Cell, 深度學習訓練完成後,用MQTT Publish通知訊息，告知Web Server有模組己更新，並且更新Web Server結果。

2022.05.23 新增sub-ml.py
   -- 此段程式放在 Web Server 裡的 shell_script 資料夾裡面，下載從 ML Server 裡的執行結果。

2022.06.28 設定排程
   -- 監聽 訂閱程式 是否還有沒有執行。如果沒有，系統重新啟動。

2022.06.25 程式更新最後完成版本

2022.11.21 程式更新完成。
   -- 更新 subscribe 程式。
   -- TOPIC elec110, elec220, plug1-1, plug1-2, plug1-3, plug3-1, plug3-2, plug3-3
   -- 新增 api/status。
