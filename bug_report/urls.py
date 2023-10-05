from django.urls import include,path
from . import views


app_name = "report"
urlpatterns = [
    path('', views.reportar_bug, name='reportar_bug'),
    path('confirmacion_reporte', views.confirmacion_reporte, name='confirmacion_reporte'),
]