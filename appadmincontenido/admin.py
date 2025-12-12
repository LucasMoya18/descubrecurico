from django.contrib import admin
from .models import Evento, Articulo, Noticia, Reportaje, Actividad, Categoria, Comentario, BloqueArticulo, BloqueNoticia, BloqueReportaje

# Configuración básica
admin.site.register(Evento)
admin.site.register(Actividad)
admin.site.register(Categoria)
admin.site.register(Comentario)

# Configuración con Inlines para los bloques de contenido
class BloqueArticuloInline(admin.StackedInline):
    model = BloqueArticulo
    extra = 0

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    inlines = [BloqueArticuloInline]
    list_display = ('titulo', 'autor', 'estado', 'publicado_en')

class BloqueNoticiaInline(admin.StackedInline):
    model = BloqueNoticia
    extra = 0

@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    inlines = [BloqueNoticiaInline]
    list_display = ('titulo', 'autor', 'estado', 'publicado_en')

class BloqueReportajeInline(admin.StackedInline):
    model = BloqueReportaje
    extra = 0

@admin.register(Reportaje)
class ReportajeAdmin(admin.ModelAdmin):
    inlines = [BloqueReportajeInline]
    list_display = ('titulo', 'autor', 'estado', 'publicado_en')
