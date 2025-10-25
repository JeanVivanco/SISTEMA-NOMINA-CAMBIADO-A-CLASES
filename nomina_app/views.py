from django import forms
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from .models import Empleado, Nomina, NominaDetalle
from .forms import EmpleadoForm, NominaForm, NominaDetalleForm
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# VISTAS BASADAS EN CLASES DE NOMINA_APP
######################## Empleado ########################
class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'nomina/empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Empleado.objects.filter(nombre__icontains=query)
        return Empleado.objects.all()


class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'nomina/empleado_form.html'
    success_url = reverse_lazy('nomina_app:empleado_list')

class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'nomina/empleado_form.html'
    success_url = reverse_lazy('nomina_app:empleado_list')

class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'nomina/empleado_delete.html'
    success_url = reverse_lazy('nomina_app:empleado_list')

###################### Nómina #########################
class NominaListView(LoginRequiredMixin, ListView):
    model = Nomina
    template_name = 'nomina/nomina_list.html'
    context_object_name = 'nominas'
    paginate_by = 10

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Nomina.objects.filter(aniomes__icontains=query)
        return Nomina.objects.all()


class NominaCreateView(LoginRequiredMixin, CreateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'nomina/nomina_form.html'
    success_url = reverse_lazy('nomina_app:nomina_list')

class NominaDetailView(LoginRequiredMixin, DetailView):
    model = Nomina
    template_name = 'nomina/nomina_detail.html'
    context_object_name = 'nomina'

class NominaUpdateView(LoginRequiredMixin, UpdateView):
    model = Nomina
    form_class = NominaForm
    template_name = 'nomina/nomina_form.html'
    success_url = reverse_lazy('nomina_app:nomina_list')

class NominaDeleteView(LoginRequiredMixin, DeleteView):
    model = Nomina
    template_name = 'nomina/nomina_delete.html'
    success_url = reverse_lazy('nomina_app:nomina_list')

#Detalle de Nómina
class NominaDetalleCreateView(LoginRequiredMixin, CreateView):
    model = NominaDetalle
    form_class = NominaDetalleForm
    template_name = 'nomina/nomina_detalle_form.html'
    
    def get_success_url(self):
        return reverse_lazy('nomina_detail', kwargs={'pk': self.kwargs['nomina_id']})
    
    def form_valid(self, form):
        form.instance.nomina = get_object_or_404(Nomina, pk=self.kwargs['nomina_id'])
        return super().form_valid(form)

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'nomina/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ultima_nomina = Nomina.objects.order_by('-aniomes').first()
        context['ultima_nomina'] = ultima_nomina
        context['detalles'] = ultima_nomina.detalles.all() if ultima_nomina else []
        context['total_empleados'] = Empleado.objects.count()
        context['total_neto_mes'] = ultima_nomina.neto if ultima_nomina else 0
        context['promedio_sueldo'] = Empleado.objects.aggregate(promedio=Avg('sueldo'))['promedio']
        return context

######################  APARTADO PARA EL LOGIN #########################
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Avg

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('nomina_app:dashboard')
        else:
            messages.error(request, 'Credenciales inválidas 🤮')
    return render(request, 'nomina/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Sesión cerrada 🦦')
    return redirect('nomina_app:login')
