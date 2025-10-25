from django.db import models

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
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    neto = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Nómina {self.aniomes} - Neto: {self.neto}"

class NominaDetalle(models.Model):
    nomina = models.ForeignKey(Nomina, on_delete=models.CASCADE, related_name='detalles')
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    sueldo = models.DecimalField(max_digits=10, decimal_places=2)
    bono = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_ing = models.DecimalField(max_digits=10, decimal_places=2)
    iess = models.DecimalField(max_digits=10, decimal_places=2)
    prestamo = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tot_des = models.DecimalField(max_digits=10, decimal_places=2)
    neto = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.tot_ing = self.sueldo + self.bono
        self.tot_des = self.iess + self.prestamo
        self.neto = self.tot_ing - self.tot_des
        super().save(*args, **kwargs)
        # Actualizar totales en la nómina asociada
        nomina = self.nomina
        nomina.tot_ing += self.tot_ing
        nomina.tot_des += self.tot_des
        nomina.neto += self.neto
        nomina.save()





    


