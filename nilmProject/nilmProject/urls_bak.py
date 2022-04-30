"""nilmProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, re_path, url, handler404
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

#from sensor.views import SensorViewSet    #REST API --Sensor
from sensor.views import getObjectInfo    #REST API --Sensor
from interface.views import redirectWeb   #Sensor Web Interface Page
from stream.views import eventsource

from nilm.views import showInfo, getChartData, getChartDataJson
from ukdale.views import showInfo1, getChartDataJson1
from iawe.views import showInfo2, getChartDataJson2

from analyze.views import redirectionPage, showResult   #Analyze Interface Page

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^sensor/', redirectWeb),      #sensor 頁面
    url(r'^stream/', getObjectInfo), #產出圖表資料
#    url(r'^api/sensor/', SensorViewSet.as_view()), #sensor Data
#    url(r'^api/', include(router.urls)), #REST API
#    url(r'^eventsource/', eventsource), #Server Sent Event
#    url(r'^/', TemplateView.as_view(template_name="index_sensor.html")),           #顯示的頁面
    url(r'^redd/', showInfo),           #REDD 資訊
    url(r'^reddataset/', getChartDataJson), #產出圖表資料
    url(r'^ukdale/', showInfo1),        #ukdale 資訊
    url(r'^ukdataset/', getChartDataJson1), #產出圖表資料
    url(r'^iawe/', showInfo2),          #iawe 資訊
    url(r'^iawedataset/', getChartDataJson2), #產出iAWE圖表資料
    url(r'^analyze/', redirectionPage),       #analyze 頁面
    url(r'^predict/', showResult),       #analyze 頁面
]
