from django.db import models
from django.contrib.auth.models import User
import uuid

class Sensor_Group(models.Model):
    group_id = models.AutoField(verbose_name='Group Id', primary_key=True)
    group_name = models.CharField(verbose_name='Group Name', max_length=50) 
    group_type = models.CharField(verbose_name='Group Type', max_length=50) 
    group_discription = models.TextField(verbose_name='Group Discription')
    date_created = models.DateTimeField(verbose_name='Date Created',auto_now_add=True)
    user = models.ForeignKey(User, verbose_name='User', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.group_id) +' - '+ str(self.group_name)


class Sensors(models.Model):

    key = models.CharField(verbose_name= "API Key" , max_length=50, unique=True)
    sensor_name = models.CharField(verbose_name= "Sensor Name" , max_length=100)
    sensor_type = models.CharField(verbose_name= "Sensor Type" , max_length=100)
    sensor_description = models.TextField(verbose_name="Sensor Discription")
    date_created = models.DateTimeField(verbose_name='Date Created',auto_now_add=True)
    sensor_group = models.ForeignKey(Sensor_Group, verbose_name='Sensor Group', on_delete=models.SET_NULL, null=True)
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
