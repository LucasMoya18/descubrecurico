from django.core.management.base import BaseCommand
from applogin.models import Rol


class Command(BaseCommand):
    help = 'Crear roles por defecto en el sistema'

    def handle(self, *args, **options):
        roles_data = [
            {'nombre': 'admin', 'descripcion': 'Administrador del sistema'},
            {'nombre': 'socio', 'descripcion': 'Socio del gremio'},
            {'nombre': 'empresa', 'descripcion': 'Empresa del gremio'}
        ]
        
        for rol_data in roles_data:
            rol, created = Rol.objects.get_or_create(
                nombre=rol_data['nombre'],
                defaults={'descripcion': rol_data['descripcion']}
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Rol "{rol.get_nombre_display()}" creado exitosamente')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Rol "{rol.get_nombre_display()}" ya existe')
                )
