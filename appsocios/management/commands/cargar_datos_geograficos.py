import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from appsocios.models import Region, Provincia, Comuna

class Command(BaseCommand):
    help = 'Carga datos de regiones, provincias y comunas desde paisdata.json'

    def handle(self, *args, **kwargs):
        # Construir la ruta al archivo JSON
        # Asumimos que BASE_DIR es la carpeta donde está manage.py
        json_path = os.path.join(settings.BASE_DIR, 'appsocios', 'static', 'css', 'datos', 'paisdata.json')

        if not os.path.exists(json_path):
            self.stdout.write(self.style.ERROR(f'No se encontró el archivo en: {json_path}'))
            return

        self.stdout.write(self.style.WARNING('Iniciando carga de datos...'))

        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # 1. Cargar Regiones
            self.stdout.write('Procesando Regiones...')
            for item in data['regiones']:
                Region.objects.update_or_create(
                    id=item['id'],
                    defaults={
                        'region': item['region'],
                        'abreviatura': item['abreviatura'],
                        'capital': item['capital']
                    }
                )

            # 2. Cargar Provincias
            self.stdout.write('Procesando Provincias...')
            for item in data['provincias']:
                # Obtenemos la instancia de la región relacionada
                region = Region.objects.get(id=item['region_id'])
                Provincia.objects.update_or_create(
                    id=item['id'],
                    defaults={
                        'provincia': item['provincia'],
                        'region': region
                    }
                )

            # 3. Cargar Comunas
            self.stdout.write('Procesando Comunas...')
            for item in data['comunas']:
                # Obtenemos la instancia de la provincia relacionada
                provincia = Provincia.objects.get(id=item['provincia_id'])
                Comuna.objects.update_or_create(
                    id=item['id'],
                    defaults={
                        'comuna': item['comuna'],
                        'provincia': provincia
                    }
                )

            self.stdout.write(self.style.SUCCESS('¡Datos geográficos cargados exitosamente!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ocurrió un error: {str(e)}'))
