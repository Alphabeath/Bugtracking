from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

# Create your tests here.

class RegistrationTestCase(TestCase):

    def setUp(self):
        self.username = "testuser"
        self.password = "testpassword123"
        self.email = "test@email.com"

        self.user = get_user_model().objects.create_user(
            self.username,
            self.email,
            self.password
        )

    def test_signup_view_normal(self):
        # Prueba que al registrar un usuario, se crea un usuario en la base de datos

        new_username = "newtestuser"
        new_password = "newtestpassword123"
        new_email = "newtest@email.com"

        response = self.client.post(reverse('home:signup'), {
            'username': new_username,
            'email': new_email,
            'password1': new_password,
            'password2': new_password
        })

        self.assertEqual(response.status_code, 302) # Comprueba que se redirige despues de un POST
        self.assertTrue(User.objects.filter(username=new_username).exists()) # Comprueba que se crea un usuario en la base de datos

    def test_signup_view_invalid(self):
        # Prueba registrar usuario con datos invalidos
        
        response = self.client.post(reverse('home:signup'), {
            'username': 'invalid_username',
            'email': 'invalid_email',
            'password1': 'short',  # Contraseña demasiado corta
            'password2': 'short',  # Contraseña demasiado corta
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='invalid_username').exists())  # Verifica que no se creó un usuario

    def test_signup_view_empty(self):
        # Prueba registrar usuario con campos vacios
        
        response = self.client.post(reverse('home:signup'), {
            'username': '',
            'email': '',
            'password1': '',
            'password2': '',
        })

        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username='').exists())

    def test_login_view_normal(self):
        # Prueba que al iniciar sesión con un usuario existente, se redirige a la pagina principal

        response = self.client.post(reverse('home:login'), {
            'username': self.username,
            'password': self.password
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.client.login(username=self.username, password=self.password))

    def test_login_view_invalid(self):
        # Prueba iniciar sesión con datos invalidos

        response = self.client.post(reverse('home:login'), {
            'username': 'invalid_username',
            'password': 'invalid_password'
        })

        self.assertEqual(response.status_code, 302) 
        self.assertFalse(self.client.login(username='invalid_username', password='invalid_password'))

    def test_login_view_empty(self):
        # Prueba iniciar sesión con campos vacios

        response = self.client.post(reverse('home:login'), {
            'username': '',
            'password': ''
        })

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.client.login(username='', password=''))

    def test_logout_view(self):
        # Prueba cerrar sesión

        self.client.login(username=self.username, password=self.password)
        
        response = self.client.get(reverse('home:exit'))

        self.assertEqual(response.status_code, 302)

        user = self.client.session.get('_auth_user_id')
        self.assertFalse(user)