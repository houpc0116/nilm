from rest_framework import serializers
from sensor.models import Sensor

class SensorSerializer(serializers.ModelSerializer):
#   SerializerMethodField 這是一個只讀欄位。
#	days_since_created = serializers.SerializerMethodField()
    class Meta:
        model = Sensor
        fields = '__all__'
#        fields = ('id', 'song', 'singer', 'last_modify_date', 'created')