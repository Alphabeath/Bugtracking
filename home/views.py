from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib import messages
from .models import ReporteBug, Bug
from database.models import ReporteBug, Bug, Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import CustomUserCreationForm
# Create your views here.


def home(request):

    if(request.user.is_authenticated == True):
        """ reportes_usuario = ReporteBug.objects.filter(id_usuario=request.user.id).order_by("-fecha_reporte")[:5].select_related("id_proyecto") """
        usuario = Usuario.objects.get(user_id=request.user.id)
        reportes_usuario = ReporteBug.objects.filter(id_usuario = usuario.id)
        

        reportes_usario_id = reportes_usuario.values_list('id_reporte', flat=True)
        reportes_solucionados = Bug.objects.filter(id_bug__in=reportes_usario_id, estado="SOLUCIONADO").count()

        reportes_asignados= Bug.objects.filter(id_bug__in=reportes_usario_id, estado="ASIGNADO").count()
        reportes_enproceso= Bug.objects.filter(id_bug__in=reportes_usario_id, estado="EN PROCESO").count()
        context = {
            "reportes_usuario": reportes_usuario,
            "reportes_solucionados": reportes_solucionados,
            "reportes_asignados": reportes_asignados,
            "reportes_enproceso": reportes_enproceso
        }
        return render(request,'home/start.html',context)
    else:
        listar_reportes = ReporteBug.objects.order_by("-fecha_reporte")[:5].select_related("id_proyecto")
        total_report = ReporteBug.objects.count()
        total_bug = Bug.objects.count()
        listar_bug = Bug.objects.order_by("-fecha_reporte")[:5].select_related("id_proyecto")


        context = {
            "listar_reportes": listar_reportes,
            "listar_bug": listar_bug,
            "total_report": total_report,
            "total_bug": total_bug
        }
        return render(request, 'home/start.html', context)
    
    

@login_required
def login(request):
    return redirect('home:principal')

def exit(request):
    logout(request)
    return redirect('home:principal')

def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save() #guarda el usuario
            return redirect('home:login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

# def home_inicio(request):
#     listar_reportes = ReporteBug.objects.order_by("id_reporte")[:20]

#     listar_bug = Bug.objects.order_by("id_bug")[:20]

#     context = {
#         "listar_reportes": listar_reportes,
#         "listar_bug": listar_bug
#     }
#     return render(request, "home/index.html", context)
