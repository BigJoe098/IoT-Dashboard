from django.urls import path
from . import views

app_name = 'dash'

urlpatterns = [
    
    #Sensor
    path('sensor/create/', views.sensor_create, name='sensor_create'),
    path('sensor/dashboard/', views.sensor_dashboard, name='sensor_dashboard'),
    path('sensor/view/', views.sensor_view, name='sensor_view'),
    path('sensor/edit/', views.sensor_edit, name='sensor_edit'),
    path('sensor/delete/', views.sensor_delete, name='sensor_delete'),
    path('sensor/data/', views.sensor_data, name='sensor_data'),
    path('sensor/data/get/', views.sensor_get, name='sensor_get'),

    #Sensor Group
    path('group/create/', views.group_create, name='group_create'),
    path('group/dashboard/', views.group_dashboard, name='group_dashboard'),
    path('group/view/', views.group_view, name='group_view'),
    path('group/edit/', views.group_edit, name='group_edit'),
    path('group/delete/', views.group_delete, name='group_delete'),
    
    #Login/Logout
    path('logout/', views.logout_user, name='logout_user'),
    path('', views.login_user, name='login'),

    # Download data
    path('download_data/<str:file_format>/<str:sensor_key>/', views.download_data, name='download_data'),
    path('download_group_data/<str:file_format>/<str:group_id>/', views.download_group_data, name='download_group_data'),
]
