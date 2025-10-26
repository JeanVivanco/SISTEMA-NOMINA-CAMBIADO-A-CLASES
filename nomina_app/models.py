from django.db import models
from decimal import Decimal
from django.db.models import Sum

# LOS MODELOS SON LAS TABLAS DE LA BASE DE DATOS
class Empleado(models.Model):
    cedula = models.CharField(max_length=10, unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    departamento = models.CharField(max_length=100)
    cargo = models.CharField(max_length=100)
    fecha_contratacion = models.DateField()

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.cedula}"

class Nomina(models.Model):
    aniomes = models.CharField(max_length=6)  # Ej: '202401'
    tot_ing = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    tot_des = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal('0.00'))
    neto = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))

    def __str__(self):
        return f"Nómina {self.aniomes} - Neto: {self.neto}"
    
    def save(self, *args, **kwargs):
        self.neto = (self.tot_ing or Decimal('0.00')) - (self.tot_des or Decimal('0.00'))
        super().save(*args, **kwargs)

    def recalcular_totales(self):
        """Recalcula los totales a partir de sus detalles."""
        agregados = self.detalles.aggregate(Sum('tot_ing'), Sum('tot_des'), Sum('neto'))
        self.tot_ing = agregados['tot_ing__sum'] or Decimal('0.00')
        self.tot_des = agregados['tot_des__sum'] or Decimal('0.00')
        self.save()


class NominaDetalle(models.Model):
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name='detalles')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    bono = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    iess = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    prestamo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    neto = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Cálculos del detalle
        self.iess = self.sueldo * Decimal('0.0945') # 9.45% IESS
        self.tot_ing = self.sueldo + self.bono
        self.tot_des = self.iess + self.prestamo
        self.neto = self.tot_ing - self.tot_des
        
        is_new = self.pk is None # Guardar si es un nuevo objeto
        super().save(*args, **kwargs) # Guardar el detalle primero

        # Recalcular los totales en la nómina padre
        if is_new or self.nomina:
            self.nomina.recalcular_totales()
