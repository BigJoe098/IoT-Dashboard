from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *
from django.http import JsonResponse, HttpResponse
from datetime import datetime
import csv


"""
#####################################################################

Login/Logout                        

#####################################################################
"""

def login_user(request):
    if request.method == 'POST':
        username = request.POST['user']
        password = request.POST['pass']
        logout(request)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/sensor/dashboard")
        else:
            messages.error(request, "Invalid username or password, Please try again.")
            return redirect('/')
    else:
        return render(request, "login.html")

@login_required(login_url="/")
def logout_user(request):
    logout(request)
    return redirect('/')


"""
#####################################################################

Sensor

#####################################################################
"""

#Dashboard for the sensor
@login_required(login_url="/")
def sensor_dashboard(request):
    
    result_set = Sensors.objects.filter(user=request.user)
    
    Search = request.POST.get('search')
    if Search != None and Search != "":
        result_set = result_set.filter(
            Q(sensor_name__icontains=Search) | 
            Q(sensor_type__icontains=Search) |
            Q(sensor_description__icontains=Search) |
            Q(key__icontains=Search)
        )
    
    result_set.order_by("date_created")
    
    """ NOTE: Pagination for later
    paginator = Paginator(result_set, 5)
    result_set = paginator.get_page(1)
    """

    #Setting the site dynamic data
    site_settings = {
        'active' : 'Sensors',
        'dashboard_heading' : 'Sensor Dashboard'
    }
    
    return render(request, 'sensor_dash.html', {'sensors': result_set, 'site_settings' : site_settings})

#Sensor Creation
@login_required(login_url="/")
def sensor_create(request):
    
    if request.method == 'POST':
        form = SensorsForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "Successfully Created."+item.key)
        else:
            messages.error(request, "Was Not able to create new sensor.")
        
        return redirect("/sensor/create")
    else:
        form = SensorsForm()
        site_settings = {
            'active' : 'Sensors',
            'dashboard_heading' : 'Create New Sensor'
        }
        return render(request, "sensor_create.html",{"form":form, 'site_settings' : site_settings})
    
#Sensor Editing
@login_required(login_url="")
def sensor_edit(request):
    
    key=request.GET['key']
    instance = Sensors.objects.get(key=key)
    
    if request.method == 'POST':
        form = SensorEditForm(request.POST, instance=instance)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, "Successfully Edited.")
        else:
            messages.error(request, "Was Not able to edit sensor.")
        
        return redirect("/sensor/dashboard/")
    
    else:
        form = SensorEditForm(instance=instance)
        site_settings = {
            'active' : 'Sensors',
            'dashboard_heading' : 'Edit Sensor Details'
        }
        return render(request, "sensor_edit.html",{"form":form, 'site_settings' : site_settings})

#Viewing Sensor Data
@login_required(login_url="")
def sensor_view(request):
    
    key=request.GET['key']
    instance = Sensors.objects.get(key=key)
    form = SensorViewForm(instance=instance)
    site_settings = {
        'active' : 'Sensors',
        'dashboard_heading' : 'View Sensor Details'
    }
    return render(request, "sensor_view.html",{"form":form, 'site_settings' : site_settings})

#Deleteing Sensor Data
@login_required(login_url="")
def sensor_delete(request):
    
    key=request.GET['key']
    instance = Sensors.objects.get(key=key)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect('/sensor/dashboard/')

#Function to accept sensor data 
def sensor_data(request):
    
    try:
        key=request.GET['key']
        data=request.GET['data']
        if data == None or data == '':
            raise Exception('No Data Recieved')
        instance = Sensors.objects.get(key=key)
        new_sensor_record = Sensor_Data(sensor=instance, data=data)
        new_sensor_record.save()
        json_response = {
            'status' : 'OK'
        }
    except:
        json_response = {
            'status' : 'NO'
        }
    return JsonResponse(json_response)

#function to send data to sensor
def sensor_get(request):
    
    try:
        key=request.GET['key']
        initial=request.GET['initial']
        if initial == '1':

            instance = list(
                Sensor_Data.objects.filter(sensor=Sensors.objects.get(key=key))
                .order_by('date_time')
                .values_list('data','date_time')
            )
            datas = [float(data[0]) for data in instance]
            dates = [date[1].strftime('%m/%d/%Y, %H:%M:%S.%f') for date in instance]

            json_response = {
                'datas' : datas,
                'dates' : dates
            }
            print(json_response)

            return JsonResponse(json_response)
        
        elif initial == '0':
            last_date = request.GET['date']
            if last_date == None or last_date == '':
                raise Exception('No Date Recieved')
            
            last_date = datetime.strptime(last_date, '%m/%d/%Y, %H:%M:%S.%f')

            instance = list(
                Sensor_Data.objects.filter(sensor=Sensors.objects.get(key=key), date_time__gt=last_date)
                .order_by('date_time')
                .values_list('data','date_time')
            )
            datas = [float(data[0]) for data in instance]
            dates = [date[1].strftime('%m/%d/%Y, %H:%M:%S.%f') for date in instance]

            json_response = {
                'datas' : datas,
                'dates' : dates
            }

            return JsonResponse(json_response)
        
        else:
            raise Exception('Invalid initial Data')
    except Exception as e:
        print(e)
        json_response = {
            'status' : 'NO'
        }
    return JsonResponse(json_response)

"""
#####################################################################

Sensor Group

#####################################################################
"""

@login_required(login_url="/")
def group_dashboard(request):
    
    result_set = Sensor_Group.objects.filter(user=request.user)
    
    Search = request.POST.get('search')
    if Search != None and Search != "":
        result_set = result_set.filter(
            Q(group_name__icontains=Search) | 
            Q(group_type__icontains=Search) |
            Q(group_description__icontains=Search) |
            Q(key__icontains=Search)
        )
    
    result_set.order_by("date_created")
    
    """ NOTE: Pagination for later
    paginator = Paginator(result_set, 5)
    result_set = paginator.get_page(1)
    """

    #Setting the site dynamic data
    site_settings = {
        'active' : 'Sensor_Groups',
        'dashboard_heading' : 'Sensor Group Dashboard'
    }
    
    return render(request, 'sensor_group_dash.html', {'groups': result_set, 'site_settings' : site_settings})

@login_required(login_url="/")
def group_create(request):
    
    if request.method == 'POST':
        form = SensorsGroupForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.user = request.user
            item.save()
            messages.success(request, "Successfully Created.")
        else:
            messages.error(request, "Was Not able to create new sensor group.")
        
        return redirect("/group/create")
    else:
        form = SensorsGroupForm()
        site_settings = {
            'active' : 'Sensor_Groups',
            'dashboard_heading' : 'Create New Sensor Group'
        }
        return render(request, "group_create.html",{"form" : form, 'site_settings' : site_settings})

#Sensor Editing
@login_required(login_url="")
def group_edit(request):
    
    key=request.GET['key']
    instance = Sensor_Group.objects.get(group_id=key)
    
    if request.method == 'POST':
        form = SensorsGroupEditForm(request.POST, instance=instance)
        
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, "Successfully Edited.")
        else:
            messages.error(request, "Was Not able to edit sensor.")
        
        return redirect("/group/dashboard/")
    
    else:
        form = SensorsGroupEditForm(instance=instance)
        site_settings = {
            'active' : 'Sensor_Groups',
            'dashboard_heading' : 'Edit Sensor Group Details'
        }
        return render(request, "group_edit.html",{"form":form, 'site_settings' : site_settings})

#Viewing Sensor Data
@login_required(login_url="")
def group_view(request):
    
    key=request.GET['key']
    instance = Sensor_Group.objects.get(group_id=key)
    form = SensorsGroupViewForm(instance=instance)
    site_settings = {
        'active' : 'Sensor_Groups',
        'dashboard_heading' : 'View Sensor Group Details'
    }
    return render(request, "group_view.html",{"form":form, 'site_settings' : site_settings})

#Deleteing Sensor Data
@login_required(login_url="")
def group_delete(request):
    
    key=request.GET['key']
    instance = Sensor_Group.objects.get(group_id=key)
    instance.delete()
    messages.success(request, "Successfully deleted")
    return redirect('/group/dashboard/')

@login_required(login_url="/")
def download_data(request, file_format, sensor_key):
    sensors = Sensors.objects.filter(key=sensor_key)
    sensor_data = Sensor_Data.objects.filter(sensor__key=sensor_key)

    if file_format == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="data-{sensor_key}.{file_format}"'
        writer = csv.writer(response)
        writer.writerow(['API Key', 'Sensor Name', 'Sensor Type', 'Sensor Description', 'Date Created', 'Sensor Group'])
        for sensor in sensors:
            writer.writerow([sensor.key, sensor.sensor_name, sensor.sensor_type, sensor.sensor_description, sensor.date_created, sensor.sensor_group])
        writer.writerow([])
        writer.writerow(['Sensor', 'Data', 'Date and Time'])
        for data in sensor_data:
            writer.writerow([data.sensor, data.data, data.date_time])
    elif file_format == 'txt':
        response = HttpResponse(content_type="text/plain")
        response['Content-Disposition'] = f'attachment; filename="data-{sensor_key}.{file_format}"'
        for sensor in sensors:
            response.write(f'API Key: {sensor.key}\nSensor Name: {sensor.sensor_name}\nSensor Type: {sensor.sensor_type}\nSensor Description: {sensor.sensor_description}\nDate Created: {sensor.date_created}\nSensor Group: {sensor.sensor_group}\n\nSensor Data:\n')
            for data in sensor_data:
                response.write(f'Data: {data.data}\nDate and Time: {data.date_time}\n')
            response.write('\n\n')
    return response
