from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *

#@login_required(login_url="")
def create_sensor(request):
    
    if request.method == 'POST':
        form = SensorsForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.save()
            messages.success(request, "Successfully Created.")    
        else:
            print(form.errors)
            messages.error(request, "Was Not able to create new teacher.")
        
        return redirect("/create/teacher")
    else:
        form = SensorsForm()
        return render(request, "Sensor.html",{"form":form})
    
def dashboard_example(request):
    return render(request, 'Dashboard.html')