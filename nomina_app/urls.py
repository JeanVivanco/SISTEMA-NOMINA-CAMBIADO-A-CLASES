from django.urls import path
from . import views
app_name = 'nomina_app'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),

    # Empleados
    path('empleados/', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('empleados/nuevo/', views.EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', views.EmpleadoDeleteView.as_view(), name='empleado_delete'),

    # Nóminas
    path('nominas/', views.NominaListView.as_view(), name='nomina_list'),
    path('nominas/nueva/', views.NominaCreateView.as_view(), name='nomina_create'),
    path('nominas/<int:pk>/', views.NominaDetailView.as_view(), name='nomina_detail'),
    path('nominas/<int:pk>/editar/', views.NominaUpdateView.as_view(), name='nomina_update'),
    path('nominas/<int:pk>/eliminar/', views.NominaDeleteView.as_view(), name='nomina_delete'),
    path('nominas/<int:nomina_id>/detalle/nuevo/', views.NominaDetalleCreateView.as_view(), name='nomina_detalle_create'),

    # Autenticación
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
