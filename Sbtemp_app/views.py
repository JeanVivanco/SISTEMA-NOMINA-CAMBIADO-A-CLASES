from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Sobretiempo
from .forms import SobretiempoForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SobretiempoListView(LoginRequiredMixin, ListView):
    model = Sobretiempo
    template_name = 'Sbtemp/sobretiempo_list.html'
    context_object_name = 'registros'
    paginate_by = 10

    def get_queryset(self):
        qs = Sobretiempo.objects.all()
        tipo = self.request.GET.get('tipo')
        desde = self.request.GET.get('desde')
        hasta = self.request.GET.get('hasta')
        empleado = self.request.GET.get('empleado')

        if tipo:
            qs = qs.filter(tipo_sobretiempo__codigo=tipo)
        if desde and hasta:
            qs = qs.filter(fecha_registro__range=[desde, hasta])
        if empleado:
            qs = qs.filter(empleado__id=empleado)
        return qs

class SobretiempoCreateView(LoginRequiredMixin, CreateView):
    model = Sobretiempo
    form_class = SobretiempoForm
    template_name = 'Sbtemp/sobretiempo_form.html'
    success_url = reverse_lazy('sbtemp_app:sobretiempo_list')

class SobretiempoUpdateView(LoginRequiredMixin, UpdateView):
    model = Sobretiempo
    form_class = SobretiempoForm
    template_name = 'Sbtemp/sobretiempo_form.html'
    success_url = reverse_lazy('sbtemp_app:sobretiempo_list')

class SobretiempoDeleteView(LoginRequiredMixin, DeleteView):
    model = Sobretiempo
    template_name = 'Sbtemp/sobretiempo_delete.html'
    success_url = reverse_lazy('sbtemp_app:sobretiempo_list')



