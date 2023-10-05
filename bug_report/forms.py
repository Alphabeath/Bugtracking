from django import forms
from multiupload.fields import MultiFileField
from django.core.exceptions import ValidationError
from PIL import Image
from database.models import ReporteBug, Proyecto, Imagen
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import User

# class UsuarioForm(forms.ModelForm):
#     email = forms.EmailField()

#     class Meta:
#         model = Usuario
#         fields = ['email']

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         if self.instance.user_id:
#             self.fields['email'].disabled = True  # Campo de solo lectura si hay un usuario asignado
#             self.fields['email'].widget.attrs['readonly'] = True
#         else:
#             self.fields['email'].widget.attrs.pop('readonly', None)  # Permite edición si el usuario es None
#             self.fields['email'].widget.attrs['placeholder'] = 'Ingresa tu correo electrónico'

#         self.fields['email'].initial = self.instance.user_id.email if self.instance.user_id else None
    
class ReporteBugForm(forms.ModelForm):

    class Meta:
        model = ReporteBug
        fields = ['reporte']
        widgets = {
            'reporte': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Describe el problema aquí...',
                'style':'resize:none;',
                }),
        }       

class ProyectoForm(forms.ModelForm):
    nombre_proyecto = forms.ModelChoiceField(
        queryset=Proyecto.objects.all(),
        empty_label='---',
        widget=forms.Select(attrs={'class': 'form-control'}),
        to_field_name='id_proyecto',
        label='Nombre del proyecto',
        initial=None,
    )

    class Meta:
        model = Proyecto
        fields = ['nombre_proyecto']


class TituloForm(forms.ModelForm):
    class Meta:
        model = ReporteBug
        fields = ['titulo']
        widgets = {
            'titulo': forms.Textarea(attrs={
                'rows': 1,
                'placeholder': 'Resumen del problema ...',
                'style':'resize:none;',
                }),
        }

class ImagenForm(forms.ModelForm):
    imagenes = forms.FileField(widget=forms.FileInput(attrs={
        #'multiple': True,
        'class': 'form-control-file',
        'validators': [FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])],
    }), required=False)

    class Meta:
        model = Imagen
        fields = ['imagenes']
