from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
#-- Validador de RUN ---
def validar_run(run):
    run = run.upper().replace(".", "").replace("-", "")
    if not run[:-1].isdigit():
        raise ValidationError("El RUN debe tener una parte numérica válida.")
    
    cuerpo = run[:-1]
    dv = run[-1]

    suma = 0
    multiplicador = 2
    for digito in reversed(cuerpo):
        suma += int(digito) * multiplicador
        multiplicador = 2 if multiplicador == 7 else multiplicador + 1

    resto = suma % 11
    verificador = 11 - resto

    if verificador == 11:
        dv_esperado = '0'
    elif verificador == 10:
        dv_esperado = 'K'
    else:
        dv_esperado = str(verificador)

    if dv != dv_esperado:
        raise ValidationError("El RUN ingresado no es válido.")

# --- Modelo de Regiones ---
class Region(models.Model):
    region = models.CharField(max_length=64)
    abreviatura = models.CharField(max_length=4)
    capital = models.CharField(max_length=64)

    class Meta:
        db_table = 'regiones'
        verbose_name = 'Región'
        verbose_name_plural = 'Regiones'
        ordering = ['id']

    def __str__(self):
        return self.region

class Provincia(models.Model):
    provincia = models.CharField(max_length=64)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='provincias')

    class Meta:
        db_table = 'provincias'
        verbose_name = 'Provincia'
        verbose_name_plural = 'Provincias'
        ordering = ['id']

    def __str__(self):
        return self.provincia

class Comuna(models.Model):
    comuna = models.CharField(max_length=64)
    provincia = models.ForeignKey(Provincia, on_delete=models.CASCADE, related_name='comunas')

    class Meta:
        db_table = 'comunas'
        verbose_name = 'Comuna'
        verbose_name_plural = 'Comunas'
        ordering = ['id']

    def __str__(self):
        return self.comuna

# --- Modelo de Rubro ---
class Rubro(models.Model):
    id_rubro = models.AutoField(primary_key=True)
    nombre_rubro = models.CharField(max_length=150, unique=True)

    class Meta:
        db_table = 'Rubro'
        verbose_name = 'Rubro'
        verbose_name_plural = 'Rubros'
        ordering = ['nombre_rubro']

    def __str__(self):
        return self.nombre_rubro

# --- Modelo de Tipo de Comercialización ---
class TipoComercializacion(models.Model):
    id_tipo = models.AutoField(primary_key=True)
    nombre_tipo = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'TipoComercializacion'
        verbose_name = 'Tipo de comercialización'
        verbose_name_plural = 'Tipos de comercialización'
        ordering = ['nombre_tipo']

    def __str__(self):
        return self.nombre_tipo

# --- Modelo de Socios ---
class Socio(models.Model):
    socio_id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='socio')
    socio_rut = models.CharField(max_length=10, verbose_name='Rut', unique=True,validators=[validar_run])
    socio_nombre = models.CharField(max_length=50, verbose_name='Nombre')
    socio_apellido_paterno = models.CharField(max_length=50, verbose_name='Apellido Paterno')
    socio_apellido_materno = models.CharField(max_length=50, verbose_name='Apellido Materno')
    socio_celular = models.CharField(max_length=12, verbose_name='Teléfono Celular')
    socio_fijo = models.CharField(max_length=12, verbose_name='Teléfono Fijo')
    socio_correo = models.EmailField(max_length=50, verbose_name='Correo', unique=True)
    socio_direccion = models.CharField(max_length=256, verbose_name='Dirección')
    socio_numero = models.CharField(max_length=256, verbose_name='Número de Casa/Torre/Piso')
    socio_comuna = models.ForeignKey(Comuna, on_delete=models.PROTECT, verbose_name='Comuna')
    socio_region = models.ForeignKey(Region, on_delete=models.PROTECT, verbose_name='Región')
    socio_estado = models.CharField(max_length=50, verbose_name='Estado')
    socio_contraseña = models.CharField(max_length=128, verbose_name='Contraseña', blank=True, null=True)
    socio_fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'Socio'
        verbose_name = 'Socio'
        verbose_name_plural = 'Socios'
        ordering = ['socio_nombre']

    def __str__(self):
        return f"{self.socio_nombre} {self.socio_apellido_paterno}"

class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    rut = models.CharField(max_length=20, unique=True, null=True, blank=True)
    direccion_completa = models.TextField(null=True, blank=True)
    calle = models.CharField(max_length=255, null=True, blank=True)
    comuna = models.ForeignKey(
        Comuna, null=True, blank=True, on_delete=models.SET_NULL,
        db_column='comuna_id', related_name='empresas'
    )
    telefono = models.CharField(max_length=30, null=True, blank=True)
    correo = models.EmailField(max_length=255, null=True, blank=True)
    instagram = models.CharField(max_length=255, null=True, blank=True)
    facebook = models.CharField(max_length=255, null=True, blank=True)
    web = models.URLField(max_length=255, null=True, blank=True)
    foto = models.ImageField(upload_to='empresas/fotos/', null=True, blank=True)

    latitud = models.DecimalField(
        max_digits=17, decimal_places=14, null=True, blank=True,
        validators=[MinValueValidator(Decimal('-90')), MaxValueValidator(Decimal('90'))]
    )
    longitud = models.DecimalField(
        max_digits=17, decimal_places=14, null=True, blank=True,
        validators=[MinValueValidator(Decimal('-180')), MaxValueValidator(Decimal('180'))]
    )

    socio = models.ForeignKey(
        Socio, null=True, blank=True, on_delete=models.SET_NULL,
        db_column='socio_id', related_name='empresas'
    )
    rubro = models.ForeignKey(
        Rubro, null=True, blank=True, on_delete=models.SET_NULL,
        db_column='rubro_id', related_name='empresas'
    )
    tipo_comercializacion = models.ForeignKey(
        TipoComercializacion, null=True, blank=True, on_delete=models.SET_NULL,
        db_column='tipo_comercializacion_id', related_name='empresas'
    )

    # Nuevos campos para flujo de solicitud
    ESTADOS_SOLICITUD = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    ESTADOS_PAGO = [
        ('pendiente', 'Pendiente'),
        ('pagado', 'Pagado'),
    ]

    estado_solicitud = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD, default='pendiente', verbose_name='Estado Solicitud')
    encuesta_respondida = models.BooleanField(default=False, verbose_name='Encuesta Respondida')
    estado_pago = models.CharField(max_length=20, choices=ESTADOS_PAGO, default='pendiente', verbose_name='Estado Pago')
    activo = models.BooleanField(default=False, verbose_name='Activa')
    fecha_creacion = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'Empresa'
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

class Encuesta(models.Model):
    OPCIONES_SI_NO = [
        ('si', 'Sí'),
        ('no', 'No'),
    ]
    
    OPCIONES_DESCUENTO = [
        ('descuento_porcentaje', 'Descuento por porcentaje'),
        ('descuento_fijo', 'Descuento fijo'),
        ('ambos', 'Ambos'),
    ]
    
    OPCIONES_APOYO = [
        ('empresa1', 'Empresa 1'),
        ('empresa2', 'Empresa 2'),
        ('empresa3', 'Empresa 3'),
    ]
    
    id_encuesta = models.AutoField(primary_key=True)
    empresa = models.OneToOneField(
        Empresa, on_delete=models.CASCADE, related_name='encuesta', 
        db_column='empresa_id'
    )
    pregunta_1_descuento_comercializacion = models.CharField(
        max_length=2,
        choices=OPCIONES_SI_NO,
        null=True,
        blank=True,
        verbose_name='¿Ofrece descuento por comercialización?'
    )
    pregunta_2_tipo_descuento = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Descuento o beneficio (detallado) Ej: Descuento en tour, Descuento en productos, Descuento en hospedaje; etc.'
    )
    pregunta_2_porcentaje = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='¿Qué porcentaje % de descuento ofrece? (0% al 100%, puede escribir el número de porcentaje directamente en el signo %) '
    )
    pregunta_3_valor_empresa = models.TextField(
        null=True,
        blank=True,
        verbose_name='¿Qué valor aportará tu empresa tanto al gremio como a la ciudad, y cuál es tu visión sobre la colaboración para lograrlo?'
    )
    pregunta_4_empresa_referencia = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='¿Qué empresa de Descubre Curicó tiene referencia y apoya tu incorporación?'
    )
    # pregunta_6_empresas_apoyan removed per request
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Encuesta'
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"Encuesta - {self.empresa.nombre}"