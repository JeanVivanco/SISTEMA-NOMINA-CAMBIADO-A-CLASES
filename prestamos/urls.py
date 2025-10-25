from django.urls import path
from . import views

app_name = 'prestamos'
urlpatterns = [
    path('', views.prestamos_list, name='prestamos_list'),
    path('crear/', views.crear_prestamo, name='crear_prestamo'),
    path('editar/<int:pk>/', views.editar_prestamo, name='editar_prestamo'),
    path('eliminar/<int:pk>/', views.eliminar_prestamo, name='eliminar_prestamo'),
]