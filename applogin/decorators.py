from functools import wraps
from django.shortcuts import redirect, render
from .utils import es_admin, es_socio

def solo_admin(view_func):
    """
    Decorador para vistas que solo permite acceso a administradores.
    Si no está logueado -> Login.
    Si está logueado pero no es admin -> Página de Acceso Denegado.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificar si está autenticado (Django o Sesión Socio)
        esta_autenticado = request.user.is_authenticated or request.session.get('es_socio_login')
        
        if not esta_autenticado:
            return redirect('applogin:iniciar')
        
        # Solo los usuarios Django pueden ser admin
        if request.user.is_authenticated and es_admin(request.user):
            return view_func(request, *args, **kwargs)
            
        return render(request, 'acceso_denegado.html', status=403)
    return _wrapped_view

def solo_socio(view_func):
    """
    Decorador que permite acceso a socios (Django o Sesión) y administradores.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verificamos si es admin o socio (pasando request para validar sesión por RUT)
        if es_admin(request.user) or es_socio(request.user, request):
            return view_func(request, *args, **kwargs)
            
        # Si no está autenticado de ninguna forma (ni Django ni sesión socio)
        if not request.user.is_authenticated and not request.session.get('es_socio_login'):
            return redirect('applogin:iniciar')
            
        # Si está autenticado pero no tiene permisos
        return render(request, 'acceso_denegado.html', status=403)
    return _wrapped_view
