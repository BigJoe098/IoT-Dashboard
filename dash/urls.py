from django.urls import path
from . import views

app_name = 'dash'

urlpatterns = [
    
    #Sensor
    path('sensor/create/', views.sensor_create, name='sensor_create'),
    path('sensor/dashboard/', views.sensor_dashboard, name='sensor_dashboard'),
    path('sensor/view/', views.sensor_view, name='sensor_view'),

    #Sensor Group
    path('group/create/', views.group_create, name='group_create'),
    path('group/dashboard/', views.group_dashboard, name='group_dashboard'),
    
    #Login/Logout
    path('logout/', views.logout_user, name='logout_user'),
    path('', views.login_user, name='login'),

    # Download data
    path('download_data/<str:file_format>/<str:sensor_key>/', views.download_data, name='download_data'),
]
