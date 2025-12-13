from functools import wraps
from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import UsuarioRol


def tiene_rol(rol_nombre):
    """
    Decorador para verificar si el usuario tiene un rol específico.
    
    Uso:
        @tiene_rol('admin')
        def mi_vista(request):
            ...
    """
    def decorador(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('applogin:iniciar')
            
            try:
                usuario_rol = UsuarioRol.objects.get(usuario=request.user)
                if usuario_rol.rol.nombre != rol_nombre:
                    return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            except UsuarioRol.DoesNotExist:
                return HttpResponseForbidden("No tienes un rol asignado.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorador


def es_admin(user):
    """Verifica si un usuario es administrador"""
    if not user.is_authenticated:
        return False
    try:
        return user.rol_asignado.rol.nombre == 'admin'
    except:
        return False


def es_socio(user, request=None):
    """Verifica si un usuario es socio o si hay una sesión de socio activa"""
    # Primero verificar si es un usuario Django con rol de socio
    if user.is_authenticated:
        try:
            return user.rol_asignado.rol.nombre == 'socio'
        except:
            pass
    
    # Si no es usuario Django, verificar si hay sesión de socio
    if request and hasattr(request, 'session'):
        return request.session.get('es_socio_login', False)
    
    return False


def obtener_rol_usuario(user):
    """Obtiene el rol de un usuario"""
    if not user.is_authenticated:
        return None
    try:
        return user.rol_asignado.rol.nombre
    except:
        return None


def rol_context_processor(request):
    """
    Context processor que agrega información de roles a todos los templates.
    """
    es_admin = False
    es_socio = False
    rol_usuario = None
    
    if request.user.is_authenticated:
        rol_usuario = obtener_rol_usuario(request.user)
        es_admin = rol_usuario == 'admin'
        # Para socio, también verificar si hay socio_id en session
        if hasattr(request, 'session') and 'socio_id' in request.session:
            es_socio = True
        elif rol_usuario == 'socio':
            es_socio = True
    
    return {
        'es_admin': es_admin,
        'es_socio': es_socio,
        'rol_usuario': rol_usuario,
    }
