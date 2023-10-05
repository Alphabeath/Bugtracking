from django.db import models

# Create your models here.


class Bug(models.Model):
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    PRIORITY_CHOICES = [
        (HIGH, 'Alta'),
        (MEDIUM, 'Media'),
        (LOW, 'Baja'),
    ]
    nombre = models.CharField(max_length=100)
    fecha = models.DateTimeField("Fecha de publición")
    categoria = models.CharField(max_length=100)
    prioridad = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default=MEDIUM,
    )

    def __str__(self):
        return self.nombre