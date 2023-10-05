from django.db import models

# Create your models here.


class Bug(models.Model):
    PRIORIDADES_CHOICES = (
        ("baja", "Baja"),
        ("media", "Media"),
        ("alta", "Alta"),
        ("urgente", "Urgente"),
    )

    ESTADOS_CHOICES = (
        ('nuevo', 'Nuevo'),
        ('en proceso', 'En proceso'),
        ('solucionado', 'Solucionado'),
    )

    id_bug = models.AutoField(primary_key=True)
    titulo = models.CharField(
        max_length=255, null=False, verbose_name='Titulo del bug')
    descripcion = models.TextField(null=False, verbose_name='Descripción')
    prioridad = models.CharField(
        max_length=20, choices=PRIORIDADES_CHOICES, verbose_name='Prioridad')
    estado = models.CharField(
        max_length=20, choices=ESTADOS_CHOICES, verbose_name='Estado')
    fecha_reporte = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de reporte')

    def __str__(self):
        return str(self.id_bug)


class ReporteBug(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    titulo = models.CharField(
        max_length=255, null=False, verbose_name='titulo del reporte')
    reporte = models.TextField(null=False)
    fecha_reporte = models.DateTimeField(
        auto_now_add=True, verbose_name='Fecha de reporte')

    def __str__(self):
        return str(self.titulo)
