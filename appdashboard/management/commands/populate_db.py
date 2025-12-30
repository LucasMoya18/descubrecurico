import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth.models import User
from appsocios.models import (
    Socio, Empresa, Rubro, TipoComercializacion, 
    Region, Provincia, Comuna
)
from appadmincontenido.models import (
    Articulo, Noticia, Reportaje, Evento, Actividad, Categoria
)

class Command(BaseCommand):
    help = "Poblar la base de datos con datos de prueba (Socios, Empresas, Contenido)"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("Iniciando población de datos..."))

        # --- 1. Asegurar Datos Geográficos Básicos ---
        # Si no hay regiones, creamos una por defecto para que no falle
        if not Region.objects.exists():
            r = Region.objects.create(region="Maule", abreviatura="MA", capital="Talca")
            p = Provincia.objects.create(provincia="Curicó", region=r)
            Comuna.objects.create(comuna="Curicó", provincia=p)
            Comuna.objects.create(comuna="Molina", provincia=p)
            Comuna.objects.create(comuna="Teno", provincia=p)
            self.stdout.write("-> Datos geográficos básicos creados.")

        comunas = list(Comuna.objects.all())
        regiones = list(Region.objects.all())

        # --- 2. Rubros y Tipos de Comercialización ---
        rubros_names = ['Gastronomía', 'Turismo Aventura', 'Hotelería', 'Comercio Local', 'Vinos y Licores', 'Artesanía']
        for name in rubros_names:
            Rubro.objects.get_or_create(nombre_rubro=name)
        rubros = list(Rubro.objects.all())

        tipos_names = ['Venta en local', 'E-commerce', 'Distribución', 'Servicios']
        for name in tipos_names:
            TipoComercializacion.objects.get_or_create(nombre_tipo=name)
        tipos = list(TipoComercializacion.objects.all())

        # --- 3. Crear 10 Socios ---
        self.stdout.write("-> Creando/Verificando 10 Socios...")
        socios_creados = []
        for i in range(1, 11):
            username = f"socio_test_{i}"
            email = f"socio{i}@descubrecurico.cl"
            
            # Crear Usuario Django
            user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            if created:
                user.set_password("pass1234")
                user.save()

            # Generar RUT válido (Algoritmo Módulo 11)
            rut_base = random.randint(10000000, 25000000)
            rut_str = str(rut_base)
            suma = sum(int(d) * f for d, f in zip(reversed(rut_str), [2,3,4,5,6,7]*2))
            resto = suma % 11
            dv = 11 - resto
            if dv == 11: dv_char = '0'
            elif dv == 10: dv_char = 'K'
            else: dv_char = str(dv)
            rut_final = f"{rut_base}-{dv_char}"

            # Crear Socio
            if not hasattr(user, 'socio'):
                socio = Socio.objects.create(
                    usuario=user,
                    socio_rut=rut_final,
                    socio_nombre=f"Socio {i}",
                    socio_apellido_paterno=f"ApellidoP{i}",
                    socio_apellido_materno=f"ApellidoM{i}",
                    socio_celular=f"9{random.randint(10000000, 99999999)}",
                    socio_fijo=f"2{random.randint(2000000, 2999999)}",
                    socio_correo=email,
                    socio_direccion=f"Calle de Prueba {i*10}",
                    socio_numero=str(i*5),
                    socio_comuna=random.choice(comunas),
                    socio_region=random.choice(regiones),
                    socio_estado="Activo"
                )
                socios_creados.append(socio)
            else:
                socios_creados.append(user.socio)

        # --- 4. Crear 10 Empresas ---
        self.stdout.write("-> Creando 10 Empresas...")
        for i in range(1, 11):
            nombre_empresa = f"Empresa Ejemplo {i}"
            if not Empresa.objects.filter(nombre=nombre_empresa).exists():
                Empresa.objects.create(
                    nombre=nombre_empresa,
                    rut=f"{random.randint(50000000, 90000000)}-{random.randint(0,9)}",
                    direccion_completa=f"Avenida Siempre Viva {i*123}",
                    calle=f"Avenida Siempre Viva {i*123}",
                    comuna=random.choice(comunas),
                    telefono=f"+569{random.randint(10000000, 99999999)}",
                    correo=f"contacto@empresa{i}.cl",
                    socio=random.choice(socios_creados),
                    rubro=random.choice(rubros),
                    tipo_comercializacion=random.choice(tipos),
                    estado_solicitud='aprobada',
                    estado_pago='pagado',
                    activo=True,
                    encuesta_respondida=True,
                    fecha_creacion=timezone.now() - timedelta(days=random.randint(1, 100))
                )

        # --- 5. Categorías de Contenido ---
        cats_names = ['Cultura', 'Vinos', 'Deportes', 'Naturaleza', 'Historia']
        categorias = []
        for c in cats_names:
            obj, _ = Categoria.objects.get_or_create(nombre=c)
            categorias.append(obj)

        # --- 6. Crear Artículos, Noticias, Reportajes (10 de cada uno) ---
        self.stdout.write("-> Creando Artículos, Noticias y Reportajes...")
        
        def crear_posts(Modelo, prefijo):
            for i in range(1, 11):
                titulo = f"{prefijo} #{i}: Descubriendo el Maule"
                if not Modelo.objects.filter(titulo=titulo).exists():
                    post = Modelo.objects.create(
                        titulo=titulo,
                        resumen=f"Este es un resumen generado automáticamente para el {prefijo.lower()} número {i}. Contenido de prueba.",
                        autor="Equipo Descubre Curicó",
                        estado="PUBLISHED",
                        publicado_en=timezone.now() - timedelta(days=random.randint(0, 60))
                    )
                    post.categorias.add(random.choice(categorias))

        crear_posts(Articulo, "Artículo")
        crear_posts(Noticia, "Noticia")
        crear_posts(Reportaje, "Reportaje")

        # --- 7. Eventos y Actividades ---
        self.stdout.write("-> Creando Eventos y Actividades...")
        
        # Eventos (Futuros y Pasados)
        for i in range(1, 6):
            titulo = f"Fiesta del Vino {2025+i}"
            if not Evento.objects.filter(titulo=titulo).exists():
                inicio = timezone.now() + timedelta(days=random.randint(-10, 30))
                Evento.objects.create(
                    titulo=titulo,
                    descripcion="Un gran evento para disfrutar en familia con lo mejor de nuestra tierra.",
                    fecha_inicio=inicio,
                    fecha_termino=inicio + timedelta(days=2),
                    lugar="Plaza de Armas de Curicó"
                )

        # Actividades
        for i in range(1, 6):
            titulo = f"Taller de Cata #{i}"
            if not Actividad.objects.filter(titulo=titulo).exists():
                inicio = timezone.now() + timedelta(days=random.randint(1, 20))
                Actividad.objects.create(
                    titulo=titulo,
                    descripcion="Aprende a catar vinos como un experto en este taller práctico.",
                    fecha_inicio=inicio,
                    fecha_termino=inicio + timedelta(hours=3),
                    lugar="Viña Local"
                )

        self.stdout.write(self.style.SUCCESS("¡Base de datos poblada exitosamente!"))
