from django.db import models
from nomina_app.models import Empleado  #Importo empleados que existe en nomina_app
# MODELOS DE SOBRE TIEMPO
class TipoSobretiempo(models.Model):
    codigo = models.CharField(max_length=10)
    descripcion = models.CharField(max_length=100)
    factor = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.descripcion
    
class Sobretiempo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_registro = models.DateField()
    tipo_sobretiempo = models.ForeignKey(TipoSobretiempo, on_delete=models.CASCADE)
    numero_horas = models.DecimalField(max_digits=6, decimal_places=2)
    valor = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    def save(self, *args, **kwargs):
        horas_mensuales = 240
        sueldo_mensual = self.empleado.sueldo
        self.valor = round((sueldo_mensual / horas_mensuales) * self.numero_horas * self.tipo_sobretiempo.factor, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.empleado.nombre} - {self.fecha_registro}"



