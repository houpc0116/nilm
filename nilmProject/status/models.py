from django.db import models

# Create your models here.
class Status(models.Model):
      datetime = models.DateTimeField()
      content = models.TextField()
      
      class Meta:
            managed = False
            db_table = 'Log'
