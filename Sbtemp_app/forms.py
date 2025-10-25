from django import forms
from .models import Sobretiempo

class SobretiempoForm(forms.ModelForm):
    class Meta:
        model = Sobretiempo
        fields = ['empleado', 'fecha_registro', 'tipo_sobretiempo', 'numero_horas']
        widgets = {
            'fecha_registro': forms.DateInput(attrs={'type': 'date'}),
        }
