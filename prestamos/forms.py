from django import forms
from .models import Prestamo, TipoPrestamo

class TipoPrestamoForm(forms.ModelForm):
    class Meta:
        model = TipoPrestamo
        fields = ['descripcion', 'tasa']
        widgets = {
            'descripcion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Descripción del tipo de préstamo'
            }),
            'tasa': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tasa de interés (%)'
            }),
        }

class PrestamoForm(forms.ModelForm):
    class Meta:
        model = Prestamo
        fields = [
            'empleado',
            'tipo_prestamo',
            'fecha_prestamo',
            'monto',
            'interes',
            'monto_pagar',
            'numero_cuotas'
        ]
        widgets = {
            'empleado': forms.Select(attrs={'class': 'form-control'}),
            'tipo_prestamo': forms.Select(attrs={'class': 'form-control'}),
            'fecha_prestamo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'monto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'interes': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'monto_pagar': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),
            'numero_cuotas': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1'
            }),
        }
