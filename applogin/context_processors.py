from .utils import es_admin, es_socio

def roles_globales(request):
    """
    Context processor para disponibilizar es_admin y es_socio en todas las plantillas
    sin necesidad de pasarlos manualmente en cada vista.
    """
    context = {
        'es_admin': False,
        'es_socio': False
    }

    if request.user.is_authenticated:
        context['es_admin'] = es_admin(request.user)
        # Pasamos request para soportar la validación completa de socio
        context['es_socio'] = es_socio(request.user, request)
    elif request.session.get('es_socio_login'):
        context['es_socio'] = True
        
    return context