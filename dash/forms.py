from django import forms
from django.forms import widgets
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
        exclude = ["key","user"]
        widgets = {
            'sensor_name': forms.TextInput(attrs={'class': ''}),
            'sensor_type': forms.TextInput(attrs={'class': ''}),
            'sensor_discription': forms.TextInput(attrs={'class': ''}),
        }   