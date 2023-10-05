from django.urls import include, path
from . import views

app_name = "buglist"
urlpatterns = [
    path('', views.index, name='bug_list'),
    # Ruta para la paginación de la lista de bugs
    path('bugs/', views.index, name='bug_list_pagination'),
    # Ruta para la paginación de los reportes
    path('reports/', views.index, name='report_list_pagination'),
]
