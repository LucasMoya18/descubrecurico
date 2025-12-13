from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from applogin.models import Rol, UsuarioRol


class Command(BaseCommand):
    help = 'Asignar rol de administrador a un usuario existente'

    def add_arguments(self, parser):
        parser.add_argument('username', type=str, help='Username del usuario a promover a admin')

    def handle(self, *args, **options):
        username = options['username']
        
        try:
            usuario = User.objects.get(username=username)
            
            # Obtener o crear el rol de administrador
            rol_admin, _ = Rol.objects.get_or_create(
                nombre='admin',
                defaults={'descripcion': 'Administrador del sistema'}
            )
            
            # Asignar o actualizar el rol
            usuario_rol, created = UsuarioRol.objects.get_or_create(
                usuario=usuario,
                defaults={'rol': rol_admin}
            )
            
            if not created:
                usuario_rol.rol = rol_admin
                usuario_rol.save()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol de administrador actualizado para "{username}"')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Rol de administrador asignado a "{username}"')
                )
                
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'✗ Usuario "{username}" no encontrado')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Error: {str(e)}')
            )
