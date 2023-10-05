from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import RequestFactory
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.contrib import admin
from .models import *
from database.admin import ReasignacionBugAdmin, ReporteBugAdmin, ProgramadorAdmin, UsuarioAdmin, CargoAdmin, BugAdmin, AvancesInline, ImagenAdmin, AvancesAdmin, NotificacionesAdmin
from django.test import RequestFactory
from django.contrib.admin.sites import AdminSite

# Create your tests here.

        

class ReasignacionBugAdminTestCase(TestCase):
    def setUp(self):
        # Configura el sitio de administración
        self.site = AdminSite()
        self.reasignacion_admin = ReasignacionBugAdmin(Reasignacion, self.site)

        # Crea usuarios y otros objetos necesarios
        self.user1 = User.objects.create_user(username='user1', password='password')
        self.user2 = User.objects.create_user(username='user2', password='password')
        self.programador1 = Programador.objects.create(user=self.user1)
        self.programador2 = Programador.objects.create(user=self.user2)
        self.proyecto = Proyecto.objects.create(nombre_proyecto='Proyecto de prueba')
        self.bug = Bug.objects.create(
            titulo='Bug de prueba',
            descripcion='Descripción del bug de prueba',
            prioridad='BAJA',
            estado='PENDIENTE',
            id_proyecto=self.proyecto,
            id_programador=self.programador1
        )
        
    # Prueba para  realizar una reasignación a un mismo empleado
    def test_reasignacion_same_person(self):
        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=self.programador1,
            estado='PENDIENTE',
            id_bug=self.bug
        )
        # Se verifica que se genere la excepción de validación y se intenta guardar la reasignación
        with self.assertRaises(ValidationError) as context:
            reasignacion.full_clean()
        # Se verifica que la excepción de validación sea el mensaje establecido
        self.assertIn("No se puede reasignar a la misma persona.", str(context.exception))
    
    # Prueba para realizar una reasignación válida a un empleado diferente
    def test_reasignacion_different_person(self):
        
        user = User.objects.create(username='usuario_prueba')
        programador2 = Programador.objects.create(user=user)


        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=programador2,
            estado='PENDIENTE',
            id_bug=self.bug
        )
        # Se guarda la reasignación
        reasignacion.full_clean()
    
    
    # Prueba para verificar actualización de bug al nuevo empleado
    def test_reasignacion_updates_bug_programador(self):
        # Realiza una reasignación válida
        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=self.programador2,
            estado='PENDIENTE',
            id_bug=self.bug
        )
        # Se guarda la reasignación y se verifica que se actualice el bug
        response = self.reasignacion_admin.save_model(request=None, obj=reasignacion, form=None, change=None)
        bug = Bug.objects.get(id_bug=self.bug.id_bug)

        # Se verifica que el bug ahora tenga el nuevo empleado asignado
        self.assertEqual(bug.id_programador, self.programador2)
    
    # Prueba para verificar actualización de solicitud de reasignación al ser aprobada
    def test_reasignacion_updates_estado(self):
        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=self.programador2,
            estado='PENDIENTE',
            id_bug=self.bug
        )

        # Se guarda la reasignación y se verifica que el estado se actualice a 'APROBADO'
        response = self.reasignacion_admin.save_model(request=None, obj=reasignacion, form=None, change=None)
        reasignacion_actualizada = Reasignacion.objects.get(id_reasignacion=reasignacion.id_reasignacion)

        # Se verifica que el estado de la reasignación ahora sea 'APROBADO'
        self.assertEqual(reasignacion_actualizada.estado, "('APROBADO', 'reasignación aprobada')")

    # Prueba para verificar actualización de solicitud de reasignación al ser desaprobada
    def test_reasignacion_desaprobada(self):
        reasignacion = Reasignacion(
            id_programador_inicial=self.programador1,
            id_programador_final=self.programador2,
            estado='PENDIENTE',
            id_bug=self.bug
        )
        reasignacion.save()

        self.reasignacion_admin.delete_model(request=None, obj=reasignacion)
        reasignacion.refresh_from_db()
        self.assertEqual(reasignacion.estado, "('DESAPROBADO', 'reasignación desaprobada')")
    

# Prueba verificación sobre permisos de cambios denegados para admin en el campo Usuario
class UsuarioAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.usuario_admin = UsuarioAdmin(Usuario, self.site) 

    def test_has_change_permission(self):
        has_change_permission = self.usuario_admin.has_change_permission(None, None)
        self.assertFalse(has_change_permission)


# Prueba verificación campo 'user' en list_display de Programador en vista de admin
class ProgramadorAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.programador_admin = ProgramadorAdmin(Programador, self.site)
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.programador = Programador.objects.create(user=self.user)

    def test_list_display(self):
        # se obtiene el list_display del administrador de Programador
        list_display = self.programador_admin.get_list_display(None)
        
        # Se verifica que 'user' esté presente en list_display
        self.assertIn('user', list_display)


class CargoAdminTestCase(TestCase):
    def setUp(self):
        # Configura el sitio de administración
        self.site = AdminSite()
        self.cargo_admin = CargoAdmin(Cargo, self.site)  # Crea una instancia de CargoAdmin

    # Prueba verificación campos correctos en list_display de Cargo en vista de admin
    def test_list_display(self):
        
        list_display = self.cargo_admin.get_list_display(None)
        
        self.assertIn('id_programador', list_display)
        self.assertIn('cargo', list_display)
        self.assertIn('id_proyecto', list_display)

    # Prueba verificación fieldsets contengan los campos esperados de Cargo en vista de admin
    def test_fieldsets(self):
        
        fieldsets = self.cargo_admin.get_fieldsets(None)
        
        expected_fieldsets = (
            ('Proyecto', {'fields': ('id_proyecto',)}),
            ('Información del programador', {'fields': ('id_programador', 'cargo')}),
        )
        
        self.assertEqual(fieldsets, expected_fieldsets)

class BugAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.bug_admin = BugAdmin(Bug, self.site)

    # Prueba verificación campos correctos en list_display de Bug en vista de admin
    def test_list_display(self):
        
        list_display = self.bug_admin.get_list_display(None)
        
        expected_display = ('id_bug', 'titulo', 'id_proyecto', 'estado', 'prioridad', 'id_programador')
        
        for field in expected_display:
            self.assertIn(field, list_display)
    
    # Prueba verificación fieldsets contengan los campos esperados de Bug en vista de admin
    def test_fieldsets(self):
        
        fieldsets = self.bug_admin.get_fieldsets(None)
        
        expected_fieldsets = (
            ('Informacion del Bug', {'fields': ('titulo', 'descripcion', 'id_proyecto', 'estado', 'prioridad')}),
            ('Personal encargado', {'fields': ('id_programador',)}),
        )
        
        self.assertEqual(fieldsets, expected_fieldsets)

    # Prueba verificación campos de búsqueda configurados correctamente
    def test_search_fields(self):
        
        search_fields = self.bug_admin.search_fields
        
        expected_search_fields = ('id_proyecto', 'id_programador')
        
        for field in expected_search_fields:
            self.assertIn(field, search_fields)

    # Prueba verificación campos de filtro configurados correctamente
    def test_list_filter(self):
        
        list_filter = self.bug_admin.list_filter
        
        expected_list_filter = ('id_proyecto', 'estado')
        
        for field in expected_list_filter:
            self.assertIn(field, list_filter)

    
class ReporteBugAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.reporte_bug_admin = ReporteBugAdmin(ReporteBug, self.site)

    # Prueba verificación campos correctos en list_display de ReporteBug en vista de admin
    def test_list_display(self):
        
        list_display = self.reporte_bug_admin.get_list_display(None)
        
        expected_display = ('id_reporte', 'titulo', 'fecha_reporte', 'id_proyecto', 'estado', 'id_bug')
        
        for field in expected_display:
            self.assertIn(field, list_display)
    
    # Prueba verificación fieldsets contengan los campos esperados de ReporteBug en vista de admin
    def test_fieldsets(self):
        fieldsets = self.reporte_bug_admin.get_fieldsets(None)
        
        expected_fieldsets = (
            ('Información entregada por el usuario', {'fields': ('titulo', 'reporte', 'id_usuario')}),
            ('Información extra', {'fields': ('estado', 'id_proyecto', 'id_bug')}),
        )
        self.assertEqual(fieldsets, expected_fieldsets)

    # Prueba verificación campos de filtro configurados correctamente
    def test_list_filter(self):
        
        list_filter = self.reporte_bug_admin.list_filter
        
        expected_list_filter = ('estado', 'id_proyecto')
        
        for field in expected_list_filter:
            self.assertIn(field, list_filter)

    # Prueba verificación vista solo de reportes de bug pendientes por parte de admin
    def test_get_queryset(self):
        
        request = None
        qs = self.reporte_bug_admin.get_queryset(request)
        self.assertQuerysetEqual(
            qs, ReporteBug.objects.filter(estado=('PENDIENTE', 'reporte en estado pendiente')), transform=lambda x: x
        )

    # Prueba verificación permisos denegados para añadir reportes de bug por parte del admin
    def test_has_add_permission(self):
        request = None
        has_permission = self.reporte_bug_admin.has_add_permission(request)
        self.assertFalse(has_permission)
    
class ImagenAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.imagen_admin = ImagenAdmin(Imagen, self.site)

    # Prueba verificación permisos denegados para añadir imagenes de bugs por parte del admin
    def test_has_add_permission(self):
        has_add_permission = self.imagen_admin.has_add_permission(None)
        self.assertFalse(has_add_permission)

    # Prueba verificación permisos denegados par modificar imagenes de bugs por parte del admin
    def test_has_change_permission(self):
        has_change_permission = self.imagen_admin.has_change_permission(None, None)
        self.assertFalse(has_change_permission)

class AvancesAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.avances_admin = AvancesAdmin(Avances, self.site)

    # Prueba verificación permisos denegados para añadir avances de empleados en bugs por parte del admin
    def test_has_add_permission(self):
        has_add_permission = self.avances_admin.has_add_permission(None)
        self.assertFalse(has_add_permission)

    # Prueba verificación permisos denegados par modificar avances de empleados en bugs por parte del admin
    def test_has_change_permission(self):
        has_change_permission = self.avances_admin.has_change_permission(None, None)
        self.assertFalse(has_change_permission)

class NotificacionesAdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()
        self.notificaciones_admin = NotificacionesAdmin(Notificaciones, self.site)

    # Prueba verificación permisos denegados par modificar notificaciones por parte del admin
    def test_has_change_permission(self):
        has_change_permission = self.notificaciones_admin.has_change_permission(None, None)
        self.assertFalse(has_change_permission)