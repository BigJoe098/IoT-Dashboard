from django.urls import path
from . import views


app_name = 'dash'

urlpatterns = [
    path('sensor/create/', views.create_sensor, name='create-sensor'),
    path('', views.dashboard_example, name='dashboard-example'),
]
