from django.urls import path
from . import views

app_name = 'sbtemp_app'

urlpatterns = [
    path('sobretiempos/', views.SobretiempoListView.as_view(), name='sobretiempo_list'),
    path('sobretiempos/nuevo/', views.SobretiempoCreateView.as_view(), name='sobretiempo_create'),
    path('sobretiempos/<int:pk>/editar/', views.SobretiempoUpdateView.as_view(), name='sobretiempo_update'),
    path('sobretiempos/<int:pk>/eliminar/', views.SobretiempoDeleteView.as_view(), name='sobretiempo_delete'),
]
