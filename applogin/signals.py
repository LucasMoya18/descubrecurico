from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from applogin.models import Rol, UsuarioRol


@receiver(post_save, sender=User)
def asignar_rol_admin_a_superuser(sender, instance, created, **kwargs):
    """
    Señal que asigna automáticamente el rol de Administrador a los superusuarios
    """
    if created and instance.is_superuser:
        # Solo procesar si es un nuevo usuario y es superuser
        try:
            # Obtener o crear el rol de administrador
            rol_admin, _ = Rol.objects.get_or_create(
                nombre='admin',
                defaults={'descripcion': 'Administrador del sistema'}
            )
            
            # Asignar el rol si no lo tiene
            if not hasattr(instance, 'rol_asignado'):
                UsuarioRol.objects.create(usuario=instance, rol=rol_admin)
        except Exception:
            # Si ocurre un error, lo ignoramos para no romper el flujo de creación del usuario
            pass
