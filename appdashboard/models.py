from django.db import models

class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha_envio = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['-fecha_envio']

    def __str__(self):
        return f"Mensaje de {self.nombre} ({self.fecha_envio})"