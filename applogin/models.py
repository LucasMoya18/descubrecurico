from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Rol(models.Model):
    TIPOS_ROL = [
        ('admin', 'Administrador'),
        ('socio', 'Socio'),
    ]
    
    nombre = models.CharField(max_length=20, choices=TIPOS_ROL, unique=True)
    descripcion = models.CharField(max_length=255, blank=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Rol'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return self.get_nombre_display()


class UsuarioRol(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rol_asignado')
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'usuario_roles'
        verbose_name = 'Usuario Rol'
        verbose_name_plural = 'Usuarios Roles'
    
    def __str__(self):
        return f"{self.usuario.username} - {self.rol.get_nombre_display()}"
