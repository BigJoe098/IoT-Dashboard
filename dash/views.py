from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
from django.db.models import Q
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import *


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

