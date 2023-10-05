from django.test import TestCase, Client
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from .forms import ReporteBugForm, ProyectoForm, TituloForm, ImagenForm
from django.contrib.auth.models import User
from database.models import ReporteBug, Proyecto, Imagen, Usuario

class ReporteBugFormTest(TestCase):
    def test_reporte_bug_form_valid(self):
        data = {'reporte': 'Este es un reporte de bug'}
        form = ReporteBugForm(data)
        self.assertTrue(form.is_valid())

    def test_reporte_bug_form_invalid(self):
        data = {}  # Data vacía, invalido
        form = ReporteBugForm(data)
        self.assertFalse(form.is_valid())

class ProyectoFormTest(TestCase):
    def test_proyecto_form_valid(self):
        proyecto = Proyecto.objects.create(nombre_proyecto='Proyecto prueba')
        data = {'nombre_proyecto': proyecto.id_proyecto}
        form = ProyectoForm(data)
        self.assertTrue(form.is_valid())

    def test_proyecto_form_invalid(self):
        data = {}  # Data vacía, invalido
        form = ProyectoForm(data)
        self.assertFalse(form.is_valid())

class TituloFormTest(TestCase):
    def test_titulo_form_valid(self):
        data = {'titulo': 'Este es un título'}
        form = TituloForm(data)
        self.assertTrue(form.is_valid())

    def test_titulo_form_invalid(self):
        data = {}  # Data vacía, invalido
        form = TituloForm(data)
        self.assertFalse(form.is_valid())

class ImagenFormTest(TestCase):
    def test_imagen_form_valid_photo(self):
        # Archivo falso
        file_data = b'fake_image_data'
        file_name = 'fake_image.jpg'
        image = SimpleUploadedFile(file_name, file_data, content_type='image/jpeg')
        data = {'imagenes': image}
        form = ImagenForm(data, {'imagenes': image})
        self.assertTrue(form.is_valid())

    def test_imagen_form_valid_no_photo(self):
        data = {}  # Data vacía, valido (se permite no subir foto)
        form = ImagenForm(data)
        self.assertTrue(form.is_valid())

##################################################

class ReporteBugViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.proyecto = Proyecto.objects.create(nombre_proyecto='Proyecto de prueba',id_proyecto=1)
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('report:reportar_bug')

    def test_reportar_bug_form_submission(self):
        data = {
            "titulo": 'Error de prueba',
            "reporte": "Reporte de prueba",
            "estado": "Pendiente",
            # La vista para enviar un bug esta bastante rara, por lo cual necesita el parametro
            # nombre_proyecto como id_proyecto (y no nombre_proyecto)
            "nombre_proyecto": 1,
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_report/reporte_bug.html')
        self.assertEqual(ReporteBug.objects.count(), 1)

    def test_reportar_bug_form_submission_with_invalid_data(self):
        data = {
            "titulo": '',  # Data invalida, no hay titulo
            "reporte": "Reporte de prueba",
            "estado": "Pendiente",
            # La vista para enviar un bug esta bastante rara, por lo cual necesita el parametro
            # nombre_proyecto como id_proyecto (y no nombre_proyecto)
            "nombre_proyecto": 1,
        }
        response = self.client.post(self.url, data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_report/reporte_bug.html')
        self.assertEqual(ReporteBug.objects.count(), 0)  # No deberian haber objetos creados