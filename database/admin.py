from typing import Optional
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.http.request import HttpRequest
from .models import *
from django.db.models import Count
from django import forms
from django.forms import ModelChoiceField
from django.utils.html import format_html

# Register your models here.



@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Programador)
class ProgramadorAdmin(admin.ModelAdmin):
    list_display = ('user',)

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('id_programador', 'cargo', 'id_proyecto')
    
    fieldsets = (
        ('Proyecto', {
            'fields': ('id_proyecto',)
        }),
        ('Información del programador', {
            'fields': ('id_programador', 'cargo')
        })
    )


class AvancesInline(admin.TabularInline):
    model = Avances

@admin.register(Bug)
class BugAdmin(admin.ModelAdmin):
    list_display  = ('id_bug', 'titulo', 'id_proyecto',
                    'estado', 'prioridad', 'id_programador')
    
    search_fields = ('id_proyecto', 'id_programador')
    
    list_filter   = ('id_proyecto', 'estado')
    
    inlines       = [
        AvancesInline,
    ]

    fieldsets     = (
        ('Informacion del Bug', {
            'fields': ('titulo', 'descripcion', 'id_proyecto', 'estado', 'prioridad')
        }),
        ('Personal encargado', {
            'fields': ('id_programador',)
        })
    )


@admin.register(ReporteBug)
class ReporteBugAdmin(admin.ModelAdmin):

    list_display = ('id_reporte','titulo', 'fecha_reporte', 'id_proyecto', 'estado', 'id_bug')
    
    list_filter  = ('estado', 'id_proyecto')
    
    fieldsets    = (
        ('Información entregada por el usuario', {
            'fields': ('titulo', 'reporte', 'id_usuario')
        }),
        ('Información extra', {
            'fields': ('estado', 'id_proyecto', 'id_bug')
        })
    )


    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado=('PENDIENTE', 'reporte en estado pendiente'))

    
    def has_add_permission(self, request,obj=None):      
        return False

    

@admin.register(Imagen)
class ImagenAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request,obj=None):
        return False
    
    def has_change_permission(self, request,obj=None):

        return False


@admin.register(Avances)
class AvancesAdmin(admin.ModelAdmin):
    
    def has_add_permission(self, request,obj=None):
        return False
    
    def has_change_permission(self, request,obj=None):
        return False


@admin.register(Notificaciones)
class NotificacionesAdmin(admin.ModelAdmin):
    def has_change_permission(self, request,obj=None):
        return False
    

class ProgramadorChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):

        total_bugs = obj.bug_set.count()
        bugs_baja = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad=('BAJA', 'bug de baja prioridad')).count()
        bugs_media = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad=('MEDIA', 'bug de media prioridad')).count()
        bugs_alta = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad=('ALTA', 'bug de alta prioridad')).count()
        bugs_urgente = obj.bug_set.filter(
            id_programador=obj.id).filter(prioridad=('URGENTE', 'bug de urgente prioridad')).count()

        return f'{obj.user.username} -  TOTAL BUGS: {total_bugs} | BAJA: {bugs_baja} | MEDIA: {bugs_media} | ALTA: {bugs_alta} | URGENTE: {bugs_urgente}'
        # return f'{obj.nombre_programador} ({obj.bug_set.count()} bugs asociados)'


class ReasignacionBugAdmin(admin.ModelAdmin):
    
    list_display = ('id_reasignacion', 'id_bug','id_programador_inicial', 'fecha_reasignacion')
    readonly_fields = ('id_programador_inicial', 'id_bug')

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
            ('Programadores involucrados', {
                'fields': ('id_programador_inicial', 'id_programador_final')
            }),

            ('Estado solicitud', {
                'fields': ('estado', 'id_bug')
            })
        )
        return fieldsets

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(estado=('PENDIENTE', 'reasignación pendiente'))

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'id_programador_final':
            kwargs['queryset'] = Programador.objects.all()
            kwargs['form_class'] = ProgramadorChoiceField
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):

        if obj.id_programador_final and obj.id_programador_inicial == obj.id_programador_final:
            messages.error(
                request, "No se puede reasignar a la misma persona.")
        else:
            if obj.id_programador_final:
                bug_id = obj.id_bug.id_bug  # Obtener el id_bug del objeto Reasignacion
                try:
                    bug = Bug.objects.get(id_bug=bug_id)
                    bug.id_programador = obj.id_programador_final
                    bug.save()
                    obj.estado = ('APROBADO', 'reasignación aprobada')
                except Bug.DoesNotExist:
                    pass
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj=None):
        obj.estado = ('DESAPROBADO', 'reasignación desaprobada')
        obj.save()

    def has_add_permission(self, request,obj=None):
        return False
    


admin.site.register(Reasignacion, ReasignacionBugAdmin)

