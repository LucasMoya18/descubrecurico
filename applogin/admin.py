from django.contrib import admin
from .models import Rol, UsuarioRol

# Register your models here.

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)

@admin.register(UsuarioRol)
class UsuarioRolAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'fecha_asignacion')
    search_fields = ('usuario__username', 'rol__nombre')
    readonly_fields = ('fecha_asignacion',)
