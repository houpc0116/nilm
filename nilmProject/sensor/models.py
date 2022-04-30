from django.db import models

# Create your models here.
class Sensor(models.Model):
    datetime = models.DateTimeField()
#    device = models.IntegerField()
    device = models.CharField(max_length=100)
    vo = models.FloatField()
    cu = models.FloatField()
    active = models.FloatField()
    reactive = models.FloatField()
    apparent = models.FloatField()
    pf = models.FloatField()
    freq = models.FloatField()
#    device = models.CharField(max_length=100)
#    house = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'sensor'