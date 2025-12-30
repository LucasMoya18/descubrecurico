from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.contrib import messages
from applogin.utils import es_admin, es_socio
from applogin.decorators import solo_admin, solo_socio
from appsocios.models import Socio, Empresa
from .models import MensajeContacto

@solo_socio
def home(request):
    if es_admin(request.user):
        # Datos para el Dashboard Admin
        ultimos_socios = Socio.objects.order_by('-socio_id')[:5]
        ultimas_empresas = Empresa.objects.select_related('rubro').order_by('-fecha_creacion')[:5]
        solicitudes_recientes = Empresa.objects.filter(estado_solicitud='pendiente').order_by('fecha_creacion')[:5]
        mensajes_no_leidos = MensajeContacto.objects.filter(leido=False).count()

        context = {
            'total_socios': Socio.objects.count(),
            'total_empresas': Empresa.objects.count(),
            'solicitudes_pendientes': Empresa.objects.filter(estado_solicitud='pendiente').count(),
            'mensajes_no_leidos': mensajes_no_leidos,
            'ultimos_socios': ultimos_socios,
            'ultimas_empresas': ultimas_empresas,
            'solicitudes_recientes': solicitudes_recientes,
            'es_admin': True,
        }
        return render(request, 'appdashboard/home.html', context)
    
    elif es_socio(request.user) or request.session.get('es_socio_login'):
        socio_id = request.session.get('socio_id')
        socio = get_object_or_404(Socio, socio_id=socio_id)
        empresas = Empresa.objects.filter(socio=socio)
        context = {'socio': socio, 'empresas': empresas}
        return render(request, 'appdashboard/home_socio.html', context)

    return redirect('home')

@solo_admin
def lista_socios(request):
    socios = Socio.objects.all().prefetch_related('empresas')
    context = {
        'socios': socios,
        'es_admin': True,
    }
    return render(request, 'appdashboard/lista_socios_admin.html', context)

@solo_admin
def detalle_socio(request, socio_id):
    try:
        socio = Socio.objects.get(socio_id=socio_id)
        empresas = socio.empresas.all()
        context = {
            'socio': socio,
            'empresas': empresas,
            'es_admin': True,
        }
        return render(request, 'appdashboard/detalle_socio_admin.html', context)
    except Socio.DoesNotExist:
        return redirect('appdashboard:lista_socios')

@solo_admin
def lista_solicitudes(request):
    # Ordenar por fecha de creación ascendente (las más antiguas primero para atenderlas antes)
    solicitudes = Empresa.objects.filter(estado_solicitud='pendiente').order_by('fecha_creacion')
    return render(request, 'appdashboard/lista_solicitudes.html', {'solicitudes': solicitudes})

@solo_admin
def gestionar_solicitud(request, empresa_id):
    empresa = get_object_or_404(Empresa, id_empresa=empresa_id)
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado_solicitud')
        nuevo_pago = request.POST.get('estado_pago')
        nuevo_activo = request.POST.get('activo')
        
        if nuevo_estado: empresa.estado_solicitud = nuevo_estado
        if nuevo_pago: empresa.estado_pago = nuevo_pago
        if nuevo_activo: empresa.activo = (nuevo_activo == 'True')
        
        empresa.save()
        
        if empresa.estado_solicitud == 'pendiente':
            return redirect('appdashboard:lista_solicitudes')
        else:
            return redirect('appdashboard:lista_empresas_admin')
        
    return render(request, 'appdashboard/detalle_solicitud.html', {'empresa': empresa})

@solo_admin
def lista_empresas_admin(request):
    # Ordenar por fecha de creación descendente (las más nuevas primero)
    empresas = Empresa.objects.all().select_related('socio', 'rubro').order_by('-fecha_creacion')
    
    # Filtros
    estado_solicitud = request.GET.get('estado_solicitud')
    estado_pago = request.GET.get('estado_pago')
    encuesta_respondida = request.GET.get('encuesta_respondida')
    activo = request.GET.get('activo')

    if estado_solicitud:
        empresas = empresas.filter(estado_solicitud=estado_solicitud)
    
    if estado_pago:
        empresas = empresas.filter(estado_pago=estado_pago)
        
    if encuesta_respondida:
        if encuesta_respondida == 'si':
            empresas = empresas.filter(encuesta_respondida=True)
        elif encuesta_respondida == 'no':
            empresas = empresas.filter(encuesta_respondida=False)
            
    if activo:
        if activo == 'si':
            empresas = empresas.filter(activo=True)
        elif activo == 'no':
            empresas = empresas.filter(activo=False)

    # Si es una petición AJAX, devolver solo las filas y el conteo
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('appdashboard/partials/lista_empresas_rows.html', {'empresas': empresas}, request=request)
        return JsonResponse({'html': html, 'count': empresas.count()})

    context = {
        'empresas': empresas,
        'filtro_solicitud': estado_solicitud,
        'filtro_pago': estado_pago,
        'filtro_encuesta': encuesta_respondida,
        'filtro_activo': activo,
    }
    return render(request, 'appdashboard/lista_empresas_admin.html', context)

@solo_admin
def eliminar_empresa_admin(request, empresa_id):
    empresa = get_object_or_404(Empresa, id_empresa=empresa_id)
    
    if request.method == 'POST':
        empresa.delete()
        return redirect('appdashboard:lista_empresas_admin')
        
    return render(request, 'appdashboard/confirmar_eliminar_empresa.html', {'empresa': empresa})

# --- Vistas de Contacto y Mensajería ---

def contacto(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        mensaje_texto = request.POST.get('mensaje')
        
        MensajeContacto.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            mensaje=mensaje_texto
        )
        messages.success(request, '¡Mensaje enviado! Nos pondremos en contacto contigo a la brevedad.')
        return redirect('contacto')
        
    return render(request, 'contacto.html')

@solo_admin
def lista_mensajes(request):
    mensajes = MensajeContacto.objects.all()
    mensajes_no_leidos = MensajeContacto.objects.filter(leido=False).count()
    return render(request, 'appdashboard/lista_mensajes.html', {
        'mensajes': mensajes, 
        'mensajes_no_leidos': mensajes_no_leidos
    })

@solo_admin
def detalle_mensaje(request, mensaje_id):
    mensaje = get_object_or_404(MensajeContacto, id=mensaje_id)
    if not mensaje.leido:
        mensaje.leido = True
        mensaje.save()
    return render(request, 'appdashboard/detalle_mensaje.html', {'mensaje': mensaje})

@solo_admin
def marcar_mensaje_leido(request, mensaje_id):
    if request.method == 'POST':
        mensaje = get_object_or_404(MensajeContacto, id=mensaje_id)
        mensaje.leido = not mensaje.leido
        mensaje.save()
        return JsonResponse({'leido': mensaje.leido})
    return JsonResponse({'error': 'Método no permitido'}, status=405)
