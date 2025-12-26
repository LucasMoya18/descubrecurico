from django.shortcuts import render, redirect, get_object_or_404
from applogin.utils import es_admin, es_socio
from applogin.decorators import solo_admin, solo_socio
from appsocios.models import Socio, Empresa

@solo_socio
def home(request):
    if es_admin(request.user):
        context = {
            'total_socios': Socio.objects.count(),
            'total_empresas': Empresa.objects.count(),
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
