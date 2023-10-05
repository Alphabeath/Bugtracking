from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from database.models import Proyecto, ReporteBug, Bug, Programador, Usuario
from django.contrib.auth import get_user_model
import re

class BuglistTestCase(TestCase):

    def setUp(self):

        # Crea un usuario de muestra
        usuario = User.objects.create_user(
            username='usuario',
            password='usuario123',
            email='usuario@usuario',
        )

        usuario_ = Usuario.objects.last()

        # Crea 5 usuarios programadores de muestra
        programadores = []
        for i in range(1, 6):
            programador = Programador.objects.create(
                user=User.objects.create_user(
                    username=f'programador{i}',
                    password=f'programador{i}123',
                    email=f'programador{i}@email',
                )
            )
            programadores.append(programador)

        # Crea 5 proyectos de muestra
        proyectos = []
        for i in range(1, 6):
            proyecto = Proyecto.objects.create(nombre_proyecto=f'Proyecto de prueba {i}')
            proyectos.append(proyecto)

        # Crea 25 reportes de bugs de muestra, asignando 5 reportes a cada proyecto
        for i in range(1, 26):
            proyecto = proyectos[(i - 1) % 5]  # Asigna 5 reportes a cada proyecto en un ciclo
            ReporteBug.objects.create(
                titulo=f'Reporte de prueba {i}',
                fecha_reporte='2023-10-01',
                id_proyecto=proyecto,
                id_usuario= usuario_,
            )

        # Crea 5 bugs de muestra, asignando 1 bug a cada proyecto
        for i in range(1, 6):
            proyecto = proyectos[i - 1]
            programador = programadores[i - 1]
            Bug.objects.create(
                titulo=f'Bug de prueba {i}',
                fecha_reporte='2023-10-01',
                estado='ASIGNADO',
                id_proyecto=proyecto,
                id_programador=programador,
            )

        # Creo otro bug para tener dos paginas en la paginacion
        Bug.objects.create(
            titulo=f'Bug de prueba 6',
            fecha_reporte='2023-10-01',
            estado='ASIGNADO',
            id_proyecto=proyectos[0],
            id_programador=programadores[0],
        )
    
    def test_view_normal(self):
        # Prueba que la vista normal se carga correctamente
        response = self.client.get(reverse('buglist:bug_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buglist/buglist.html')

    def test_buglist_view_pagination(self):
        # Prueba que la vista buglist se carga correctamente
        response = self.client.get(reverse('buglist:bug_list_pagination'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buglist/buglist.html')

    def test_reportlist_view_pagination(self):
        # Prueba que la vista reportlist se carga correctamente
        response = self.client.get(reverse('buglist:report_list_pagination'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'buglist/buglist.html')

    def test_buglist_view_pagination_page(self):
        # Prueba que la vista buglist se carga correctamente en la página 2
        response = self.client.get(reverse('buglist:bug_list_pagination') + '?bug_page=2')
        self.assertEqual(response.status_code, 200)
        
        # Extraer el contenido HTML de la respuesta
        content = response.content.decode('utf-8')  # Decodificar el contenido a una cadena UTF-8

        # Usar una expresión regular para encontrar el número de página en la clase "current-page"
        match = re.search(r'id="bug-current-page">(\d+)</span>', content)
    
        # Verificar que el número de página en el contenido de la respuesta sea el número de página correcto (en este caso, 2)
        self.assertEqual(match.group(1), '2')

    def test_buglist_view_pagination_page_invalid(self):
        # Prueba que la vista buglist muestre la última página válida cuando se ingresa un número de página inválido
        response = self.client.get(reverse('buglist:bug_list_pagination') + '?bug_page=999')
        self.assertEqual(response.status_code, 200)  # Verificar que la respuesta sea exitosa (código 200)
        
        # Extraer el contenido HTML de la respuesta
        content = response.content.decode('utf-8')

        # Usar una expresión regular para encontrar el número de página en la clase "current-page"
        match = re.search(r'id="bug-current-page">(\d+)</span>', content)

        # Verificar que el número de página sea el de la ultima pagina valida (en este caso, 2)
        self.assertEqual(match.group(1), '2')
    
    def test_reportlist_view_pagination_page(self):
        # Prueba que la vista reportlist se carga correctamente en la página 4
        response = self.client.get(reverse('buglist:report_list_pagination') + '?report_page=4')
        self.assertEqual(response.status_code, 200)
        
        # Extraer el contenido HTML de la respuesta
        content = response.content.decode('utf-8')

        # Usar una expresión regular para encontrar el número de página en la clase "current-page"
        match = re.search(r'id="report-current-page">(\d+)</span>', content)

        # Verificar que el número de página en el contenido de la respuesta sea el número de página correcto (en este caso, 4)
        self.assertEqual(match.group(1), '4')
    
    def test_reportlist_view_pagination_page_invalid(self):
        # Prueba que la vista reportlist muestre la última página válida cuando se ingresa un número de página inválido
        response = self.client.get(reverse('buglist:report_list_pagination') + '?report_page=999')
        self.assertEqual(response.status_code, 200)

        # Extraer el contenido HTML de la respuesta
        content = response.content.decode('utf-8')

        # Usar una expresión regular para encontrar el número de página en la clase "current-page"
        match = re.search(r'id="report-current-page">(\d+)</span>', content)

        # Verificar que el número de página sea el de la ultima pagina valida (en este caso, 5)
        self.assertEqual(match.group(1), '5')