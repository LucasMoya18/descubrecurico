from django.contrib.auth.management.commands.createsuperuser import Command as CreateSuperUserCommand
from django.contrib.auth.models import User
from applogin.models import Rol, UsuarioRol


class Command(CreateSuperUserCommand):
    def handle(self, *args, **options):
        # Obtener los usuarios antes de crear el superusuario
        usuarios_antes = set(User.objects.values_list('id', flat=True))
        
        # Llamar al método original para crear el superusuario
        super().handle(*args, **options)
        
        # Obtener los usuarios después de crear el superusuario
        usuarios_despues = set(User.objects.values_list('id', flat=True))
        
        # Encontrar el nuevo usuario
        nuevo_usuario_id = usuarios_despues - usuarios_antes
        
        if nuevo_usuario_id:
            usuario_id = nuevo_usuario_id.pop()
            usuario = User.objects.get(id=usuario_id)
            
            # Obtener o crear el rol de administrador
            rol_admin, _ = Rol.objects.get_or_create(
                nombre='admin',
                defaults={'descripcion': 'Administrador del sistema'}
            )
            
            # Asignar el rol de administrador al usuario
            usuario_rol, created = UsuarioRol.objects.get_or_create(
                usuario=usuario,
                defaults={'rol': rol_admin}
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'\n✓ Rol de administrador asignado automáticamente a "{usuario.username}"')
                )
            else:
                usuario_rol.rol = rol_admin
                usuario_rol.save()
                self.stdout.write(
                    self.style.SUCCESS(f'\n✓ Rol actualizado a administrador para "{usuario.username}"')
                )
