from django.shortcuts import render, redirect
from .models import Prestamo
from .forms import PrestamoForm
from django.shortcuts import get_object_or_404


# Create your views here.
def prestamos_list(request):
    prestamos = Prestamo.objects.all().order_by('-fecha_prestamo')
    return render(request, 'prestamos/prestamos_list.html', {'prestamos': prestamos})

def crear_prestamo(request):
    if request.method == 'POST':
        form = PrestamoForm(request.POST)
        if form.is_valid():
            prestamo = form.save(commit=False)
            # los cálculos los hace el modelo (en save())
            prestamo.save()
            return redirect('prestamos:prestamos_list')
    else:
        form = PrestamoForm()
    return render(request, 'prestamos/form_prestamo.html', {'form': form})

from django.shortcuts import render, get_object_or_404, redirect
from .models import Prestamo
from .forms import PrestamoForm

def editar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)  # <-- corregido
    if request.method == 'POST':
        form = PrestamoForm(request.POST, instance=prestamo)
        if form.is_valid():
            form.save()
            return redirect('prestamos:prestamos_list')
    else:
        form = PrestamoForm(instance=prestamo)
        
    return render(request, 'prestamos/form_prestamo.html', {'form': form, 'prestamo': prestamo})

def eliminar_prestamo(request, pk):
    prestamo = get_object_or_404(Prestamo, pk=pk)
    if request.method == 'POST':
        prestamo.delete()
        return redirect('prestamos:prestamos_list')
    return render(request, 'prestamos/confirmar_eliminar.html', {'prestamo': prestamo})
