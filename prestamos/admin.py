
from django.contrib import admin
from .models import TipoPrestamo, Prestamo


@admin.register(TipoPrestamo)
class TipoPrestamoAdmin(admin.ModelAdmin):
    list_display = ('id', 'descripcion', 'tasa')
    search_fields = ('descripcion',)
    list_per_page = 10


@admin.register(Prestamo)
class PrestamoAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'empleado',
        'tipo_prestamo',
        'fecha_prestamo',
        'monto',
        'interes',
        'monto_pagar',
        'numero_cuotas',
        'saldo',
    )
    list_filter = ('tipo_prestamo', 'fecha_prestamo')
    search_fields = ('empleado__nombre', 'tipo_prestamo__descripcion')
    list_per_page = 10
