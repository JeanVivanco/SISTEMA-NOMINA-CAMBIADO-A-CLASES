from django import forms
from .models import Empleado, Nomina, NominaDetalle

class EmpleadoForm(forms.ModelForm):
    class Meta:
        model = Empleado
        fields = '__all__'
        widgets = {
            'fecha_contratacion': forms.DateInput(attrs={'type': 'date'}),
        }


class NominaForm(forms.ModelForm):
    class Meta:
        model = Nomina
        fields = ['aniomes']

class NominaDetalleForm(forms.ModelForm):
    class Meta:
        model = NominaDetalle
        fields = ['empleado', 'sueldo', 'bono', 'prestamo']