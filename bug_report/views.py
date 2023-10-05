from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from bug_report.forms import ReporteBugForm, ProyectoForm, ImagenForm, TituloForm
from database.models import ReporteBug, Usuario, Proyecto, Imagen
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.

def reportar_bug(request):
    form_bug = ReporteBugForm()
    form_proyecto = ProyectoForm()
    form_imagen = ImagenForm()
    form_resumen = TituloForm()
    formulario_enviado = False

    if request.method == 'POST':
        form_bug = ReporteBugForm(request.POST)
        form_proyecto = ProyectoForm(request.POST)
        form_imagen = ImagenForm(request.POST, request.FILES)
        form_resumen = TituloForm(request.POST)

        id_proyecto = request.POST.get('nombre_proyecto')
        id_proyecto2 = Proyecto.objects.get(id_proyecto=id_proyecto)

        if form_bug.is_valid() and form_proyecto.is_valid() and form_resumen.is_valid():
            reporte_bug = form_bug.save(commit=False)
            reporte_bug.titulo = form_resumen.cleaned_data['titulo']


            usuario = Usuario.objects.get(user_id=request.user.id)
            reporte_bug.id_usuario = usuario

            reporte_bug.id_proyecto = id_proyecto2
            reporte_bug.save()

            for file in request.FILES.getlist('imagenes'):
                Imagen.objects.create(imagen=file, id_reporte=reporte_bug)

            formulario_enviado = True
            
            # Limpiar formularios después de enviar correctamente
            form_bug = ReporteBugForm()
            form_proyecto = ProyectoForm()
            form_imagen = ImagenForm()
            form_resumen = TituloForm()
        
        else:
            # Limpiar formularios
            form_bug = ReporteBugForm()
            form_proyecto = ProyectoForm()
            form_imagen = ImagenForm()
            form_resumen = TituloForm()
    else:
        form_bug = ReporteBugForm()
        form_proyecto = ProyectoForm()
        form_imagen = ImagenForm()
        form_resumen = TituloForm()

    return render(request, 'bug_report/reporte_bug.html', {'form_bug': form_bug, 'form_proyecto': form_proyecto, 'form_imagen': form_imagen, 'form_resumen': form_resumen, 'formulario_enviado': formulario_enviado})


def confirmacion_reporte(request):
    return render(request, 'bug_report/confirmacion_reporte.html')