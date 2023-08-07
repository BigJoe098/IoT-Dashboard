from django import forms
from .models import *

class CustomModelForm(forms.ModelForm):
    
    def is_valid(self):
        result = super().is_valid()

        for item in (self.fields if '__all__' in self.errors else self.errors):
            attrs = self.fields[item].widget.attrs
            attrs.update({'class': attrs.get('class', '') + ' is-invalid'})
        return result


class SensorsForm(CustomModelForm):
    
    class Meta:
        model = Sensors 
        fields = "__all__"
        exclude = ["key","user","date_created"]
        widgets = {
            'sensor_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'sensor_type': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'sensor_description': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'sensor_group' : forms.Select(attrs={'class' : 'form-select form-control-lg'})
        }   

class SensorViewForm(CustomModelForm):

    class Meta:
        model = Sensors 
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            'sensor_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'sensor_type': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'sensor_description': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'sensor_group' : forms.TextInput(attrs={'class' : 'form-control form-control-lg', 'readonly' : True}),
            'date_created' : forms.DateInput(attrs={'class' : 'form-select form-control-lg', 'readonly' : True}),
            'key' : forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True})
        }  

class SensorEditForm(CustomModelForm):

    class Meta:
        model = Sensors 
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            'sensor_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'sensor_type': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'sensor_description': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'sensor_group' : forms.TextInput(attrs={'class' : 'form-control form-control-lg'}),
            'date_created' : forms.DateInput(attrs={'class' : 'form-select form-control-lg'}),
            'key' : forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True})
        }  

class SensorsGroupForm(CustomModelForm):
    
    class Meta:
        model = Sensor_Group 
        fields = "__all__"
        exclude = ["group_id","user","date_created"]
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'group_type': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'group_discription': forms.TextInput(attrs={'class': 'form-control form-control-lg'})
        }  

class SensorsGroupViewForm(CustomModelForm):
    
    class Meta:
        model = Sensor_Group 
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'group_type': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'group_id': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'date_created': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'group_discription': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True})
        }  

class SensorsGroupEditForm(CustomModelForm):
    
    class Meta:
        model = Sensor_Group 
        fields = "__all__"
        exclude = ["user"]
        widgets = {
            'group_name': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'group_type': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'group_id': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'readonly' : True}),
            'date_created': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
            'group_discription': forms.TextInput(attrs={'class': 'form-control form-control-lg'})
        }  