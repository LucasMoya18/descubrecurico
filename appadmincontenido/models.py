from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

# --- MODELO EVENTO ---
class Evento(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()
    lugar = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ["fecha_inicio"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200]
            slug_candidate = base
            i = 1
            while Evento.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base}-{i}"
                i += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def esta_activo(self):
        """Retorna True si el evento aún no ha terminado"""
        return self.fecha_termino >= timezone.now()

# --- MODELOS DE CONTENIDO Y ACTIVIDAD ---
class Categoria(models.Model):
    nombre = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True, blank=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        ordering = ["nombre"]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.nombre)[:130] or "categoria"
            slug_candidate = base
            i = 1
            while Categoria.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base}-{i}"
                i += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

class ArticuloBase(models.Model):
    class Estado(models.TextChoices):
        BORRADOR = "DRAFT", "Borrador"
        PUBLICADO = "PUBLISHED", "Publicado"

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    resumen = models.TextField(blank=True)
    autor = models.CharField(max_length=120, default="Descubre Curicó")
    categorias = models.ManyToManyField(Categoria, related_name="%(class)s_set", blank=True)
    portada = models.ImageField(upload_to="articulos/portadas/", blank=True, null=True)
    estado = models.CharField(max_length=12, choices=Estado.choices, default=Estado.PUBLICADO)
    publicado_en = models.DateTimeField(default=timezone.now)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    comentarios = GenericRelation('Comentario')

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200]
            slug = base
            i = 1
            while self.__class__.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base}-{i}"
                i += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse(f"appadmincontenido:{self._meta.model_name}_detalle", args=[self.slug])

class Articulo(ArticuloBase):
    class Meta:
        verbose_name = "Artículo"
        verbose_name_plural = "Artículos"
        ordering = ["-publicado_en"]

    def get_type(self):
        return "Articulo"

class Noticia(ArticuloBase):
    class Meta:
        verbose_name = "Noticia"
        verbose_name_plural = "Noticias"
        ordering = ["-publicado_en"]

    def get_type(self):
        return "Noticia"

class Reportaje(ArticuloBase):
    class Meta:
        verbose_name = "Reportaje"
        verbose_name_plural = "Reportajes"
        ordering = ["-publicado_en"]

    def get_type(self):
        return "Reportaje"

class BloqueArticulo(models.Model):
    class Tipo(models.TextChoices):
        TEXTO = "TEXT", "Texto"
        SUBTITULO = "SUBTITLE", "Subtítulo"
        IMAGEN = "IMAGE", "Imagen"
        ENLACE = "URL", "Enlace"
        YOUTUBE = "YOUTUBE", "YouTube"
        VIDEO = "VIDEO", "Video (MP4/URL directa)"

    articulo = models.ForeignKey(Articulo, on_delete=models.CASCADE, related_name="bloques")
    tipo = models.CharField(max_length=12, choices=Tipo.choices, default=Tipo.TEXTO)
    orden = models.PositiveIntegerField(default=0)
    texto = models.TextField(blank=True)
    subtitulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to="articulos/bloques/", blank=True, null=True)
    pie_de_foto = models.CharField(max_length=200, blank=True)
    estilo_imagen = models.CharField(
        max_length=20,
        choices=[("default", "Default"), ("rounded", "Bordes redondeados"), ("wide", "Ancho completo"), ("shadow", "Sombra")],
        default="default",
    )
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.articulo.titulo} · {self.get_tipo_display()} · {self.orden}"

    def youtube_embed_src(self):
        if not self.url:
            return ""
        u = self.url
        if "youtu.be/" in u:
            vid = u.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{vid}"
        if "youtube.com/watch" in u and "v=" in u:
            vid = u.split("v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{vid}"
        return ""

class BloqueNoticia(models.Model):
    class Tipo(models.TextChoices):
        TEXTO = "TEXT", "Texto"
        SUBTITULO = "SUBTITLE", "Subtítulo"
        IMAGEN = "IMAGE", "Imagen"
        ENLACE = "URL", "Enlace"
        YOUTUBE = "YOUTUBE", "YouTube"
        VIDEO = "VIDEO", "Video (MP4/URL directa)"

    noticia = models.ForeignKey(Noticia, on_delete=models.CASCADE, related_name="bloques")
    tipo = models.CharField(max_length=12, choices=Tipo.choices, default=Tipo.TEXTO)
    orden = models.PositiveIntegerField(default=0)
    texto = models.TextField(blank=True)
    subtitulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to="noticias/bloques/", blank=True, null=True)
    pie_de_foto = models.CharField(max_length=200, blank=True)
    estilo_imagen = models.CharField(
        max_length=20,
        choices=[("default", "Default"), ("rounded", "Bordes redondeados"), ("wide", "Ancho completo"), ("shadow", "Sombra")],
        default="default",
    )
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.noticia.titulo} · {self.get_tipo_display()} · {self.orden}"

    def youtube_embed_src(self):
        if not self.url:
            return ""
        u = self.url
        if "youtu.be/" in u:
            vid = u.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{vid}"
        if "youtube.com/watch" in u and "v=" in u:
            vid = u.split("v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{vid}"
        return ""

class BloqueReportaje(models.Model):
    class Tipo(models.TextChoices):
        TEXTO = "TEXT", "Texto"
        SUBTITULO = "SUBTITLE", "Subtítulo"
        IMAGEN = "IMAGE", "Imagen"
        ENLACE = "URL", "Enlace"
        YOUTUBE = "YOUTUBE", "YouTube"
        VIDEO = "VIDEO", "Video (MP4/URL directa)"

    reportaje = models.ForeignKey(Reportaje, on_delete=models.CASCADE, related_name="bloques")
    tipo = models.CharField(max_length=12, choices=Tipo.choices, default=Tipo.TEXTO)
    orden = models.PositiveIntegerField(default=0)
    texto = models.TextField(blank=True)
    subtitulo = models.CharField(max_length=200, blank=True)
    imagen = models.ImageField(upload_to="reportajes/bloques/", blank=True, null=True)
    pie_de_foto = models.CharField(max_length=200, blank=True)
    estilo_imagen = models.CharField(
        max_length=20,
        choices=[("default", "Default"), ("rounded", "Bordes redondeados"), ("wide", "Ancho completo"), ("shadow", "Sombra")],
        default="default",
    )
    url = models.URLField(blank=True)

    class Meta:
        ordering = ["orden", "id"]

    def __str__(self):
        return f"{self.reportaje.titulo} · {self.get_tipo_display()} · {self.orden}"

    def youtube_embed_src(self):
        if not self.url:
            return ""
        u = self.url
        if "youtu.be/" in u:
            vid = u.split("youtu.be/")[-1].split("?")[0]
            return f"https://www.youtube.com/embed/{vid}"
        if "youtube.com/watch" in u and "v=" in u:
            vid = u.split("v=")[-1].split("&")[0]
            return f"https://www.youtube.com/embed/{vid}"
        return ""

class Comentario(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)
    object_id = models.PositiveIntegerField(null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    nombre = models.CharField(max_length=120)
    email = models.EmailField()
    texto = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado_en"]

    def __str__(self):
        return f"{self.nombre} en {self.content_object.titulo if self.content_object else 'Post'}"

class Actividad(models.Model):
    titulo = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    descripcion = models.TextField()
    fecha_inicio = models.DateTimeField()
    fecha_termino = models.DateTimeField()
    lugar = models.CharField(max_length=200, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Actividad"
        verbose_name_plural = "Actividades"
        ordering = ["fecha_inicio"]

    def __str__(self):
        return self.titulo

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.titulo)[:200]
            slug_candidate = base
            i = 1
            while Actividad.objects.filter(slug=slug_candidate).exclude(pk=self.pk).exists():
                slug_candidate = f"{base}-{i}"
                i += 1
            self.slug = slug_candidate
        super().save(*args, **kwargs)

    def esta_activa(self):
        """Retorna True si la actividad aún no ha terminado"""
        return self.fecha_termino >= timezone.now()
