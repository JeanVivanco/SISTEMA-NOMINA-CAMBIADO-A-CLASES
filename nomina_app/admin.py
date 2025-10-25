from django.contrib import admin
from .models import Empleado, Nomina, NominaDetalle

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('cedula', 'nombre', 'departamento', 'cargo', 'sueldo')
    search_fields = ('cedula', 'nombre', 'departamento', 'cargo')
    list_filter = ('departamento', 'cargo')

@admin.register(Nomina)
class NominaAdmin(admin.ModelAdmin):
    list_display = ('aniomes', 'tot_ing', 'tot_des', 'neto')
    search_fields = ('aniomes',)

@admin.register(NominaDetalle)
class NominaDetalleAdmin(admin.ModelAdmin):
    list_display = ('nomina', 'empleado', 'sueldo', 'bono', 'iess', 'prestamo', 'neto')
    list_filter = ('nomina', 'empleado')
    search_fields = ('empleado__nombre', 'nomina__aniomes')



