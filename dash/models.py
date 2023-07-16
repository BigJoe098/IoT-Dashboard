from django.db import models
from django.contrib.auth.models import User
import uuid

class Sensors(models.Model):

    key = models.CharField(verbose_name= "API Key" , max_length=50)
    sensor_name = models.CharField(verbose_name= "Sensor Name" , max_length=100)
    sensor_type = models.CharField(verbose_name= "Sensor Type" , max_length=100)
    sensor_description = models.TextField(verbose_name="Sensor Discription")
    user = models.ForeignKey(User, verbose_name="User", on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = uuid.uuid4().hex

        super(Sensors, self).save(*args, **kwargs)

    def regenerate_key(self, *args, **kwargs):
        self.key = uuid.uuid4().hex 
        self.save()

class Sensor_Data(models.Model):

    sensor = models.ForeignKey(Sensors, verbose_name="Sensor", on_delete=models.CASCADE)
    data = models.CharField("Stringified Data", max_length=500)
    date_time = models.DateTimeField("Date And Time Of Data", auto_now_add=True)
