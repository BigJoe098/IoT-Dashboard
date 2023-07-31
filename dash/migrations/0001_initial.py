# Generated by Django 4.2.3 on 2023-07-30 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Sensor_Group',
            fields=[
                ('group_id', models.AutoField(primary_key=True, serialize=False, verbose_name='Group Id')),
                ('group_name', models.CharField(max_length=50, verbose_name='Group Name')),
                ('group_type', models.CharField(max_length=50, verbose_name='Group Type')),
                ('group_discription', models.TextField(verbose_name='Group Discription')),
                ('date_created', models.DateTimeField(verbose_name='Date Created')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Sensors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50, unique=True, verbose_name='API Key')),
                ('sensor_name', models.CharField(max_length=100, verbose_name='Sensor Name')),
                ('sensor_type', models.CharField(max_length=100, verbose_name='Sensor Type')),
                ('sensor_description', models.TextField(verbose_name='Sensor Discription')),
                ('date_created', models.DateTimeField(verbose_name='Date Created')),
                ('sensor_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='dash.sensor_group', verbose_name='Sensor Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor_Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.CharField(max_length=500, verbose_name='Stringified Data')),
                ('date_time', models.DateTimeField(auto_now_add=True, verbose_name='Date And Time Of Data')),
                ('sensor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dash.sensors', verbose_name='Sensor')),
            ],
        ),
    ]
