from django.db import models

# Create your models here.
class IAWE(models.Model):
    datetime = models.DateTimeField()
    active = models.FloatField()
    reactive = models.FloatField()
    apparent = models.FloatField()
    f = models.FloatField()
    vo = models.FloatField()
    pf = models.FloatField()
    cu = models.FloatField()
    #freq = models.FloatField()
    device = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'iawe'