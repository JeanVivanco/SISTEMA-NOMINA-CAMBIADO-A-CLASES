from django.db import models
from nomina_app.models import Empleado
from decimal import Decimal, ROUND_HALF_UP


class TipoPrestamo(models.Model):
    descripcion = models.CharField(max_length=100)
    tasa = models.IntegerField(default=0)
    
    def __str__(self):
        return self.descripcion

class Prestamo(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_prestamo = models.ForeignKey(TipoPrestamo, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=10, decimal_places=2)
    monto_pagar = models.DecimalField(max_digits=10, decimal_places=2)
    numero_cuotas = models.PositiveIntegerField(default=1)
    cuota_mensual = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    

    def __str__(self):
        return f"Préstamo de {self.empleado.nombre} - {self.tipo_prestamo.descripcion}"

    def calcular_interes(self):
            """Calcula interés = monto * tasa/100"""
            if self.monto is None or self.tipo_prestamo is None:
                return Decimal('0.00')
            # tasa es entero (porcentaje)
            tasa_decimal = Decimal(self.tipo_prestamo.tasa) / Decimal('100')
            interes = (self.monto * tasa_decimal).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            return interes

    def save(self, *args, **kwargs):
        # recalcular campos derivados
        try:
            self.interes = self.calcular_interes()
        except Exception:
            self.interes = Decimal('0.00')

        try:
            self.monto_pagar = (self.monto + self.interes).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        except Exception:
            self.monto_pagar = Decimal('0.00')

        try:
            if self.numero_cuotas and self.numero_cuotas > 0:
                self.cuota_mensual = (self.monto_pagar / Decimal(self.numero_cuotas)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            else:
                self.cuota_mensual = self.monto_pagar
        except Exception:
            self.cuota_mensual = Decimal('0.00')

        # Si es creación nueva (no tiene pk aún) inicializamos saldo = monto_pagar.
        if self.pk is None:
            self.saldo = self.monto_pagar
        else:
            # Si ya existe, mantenemos el saldo actual a menos que monto_pagar haya cambiado drásticamente:
            # Simple política: si el saldo actual es 0 o mayor que monto_pagar, no lo sobreescribimos.
            # Si quieres que al actualizar el monto se resetee el saldo, comentarlo o ajustar.
            try:
                orig = Prestamo.objects.get(pk=self.pk)
                # si quieres forzar la actualización del saldo cuando cambie el monto_pagar:
                if orig.monto_pagar != self.monto_pagar:
                    # Ajustar saldo proporcionalmente (o reiniciar). Aquí lo reiniciamos:
                    self.saldo = self.monto_pagar
                else:
                    # mantener saldo anterior
                    self.saldo = orig.saldo
            except Prestamo.DoesNotExist:
                # no existía antes, setear saldo
                self.saldo = self.monto_pagar

        super().save(*args, **kwargs)