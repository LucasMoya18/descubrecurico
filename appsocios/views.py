from django.shortcuts import render, redirect, get_object_or_404
from .forms import SocioForm, RubroForm, TipoComercializacionForm, EmpresaForm, EncuestaForm
from .models import Socio, Empresa, Rubro, TipoComercializacion, Region, Comuna, Encuesta
from django.contrib import messages

def empresas(request):
    return render(request, 'appsocios/empresas.html')

def crear_socio(request):
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            socio = form.save(commit=False)
            socio.socio_estado = "Activo"  
            socio.save()
            #messages.success(request, "Socio registrado correctamente.")
            return redirect('appsocios:empresas')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = SocioForm()
    return render(request, 'appsocios/socio/crear_socio.html', {'form': form})

def crear_rubro(request):
    if request.method == 'POST':
        form = RubroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "")
            return redirect('appsocios:lista_empresas')
    else:
        form = RubroForm()
    return render(request, 'appsocios/empresa/crear_rubro.html', {'form': form})

def crear_tipo_comercializacion(request):
    if request.method == 'POST':
        form = TipoComercializacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "")
            return redirect('appsocios:lista_empresas')
    else:
        form = TipoComercializacionForm()
    return render(request, 'appsocios/empresa/crear_tipo_comercializacion.html', {'form': form})

def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES)
        if form.is_valid():
            run_socio = form.cleaned_data.get('run_socio')

            # Validar que run_socio no sea vacío en creación
            if not run_socio:
                messages.error(request, "⚠️ Debes ingresar el RUN del socio.")
                context = {
                    'form': form,
                    'regions': Region.objects.all(),
                    'comunas': Comuna.objects.all(),
                    'es_edicion': False
                }
                return render(request, 'appsocios/empresa/crear_empresa.html', context)

            # Buscar socio por RUN
            try:
                socio = Socio.objects.get(socio_rut=run_socio)
            except Socio.DoesNotExist:
                messages.error(request, "⚠️ El RUN ingresado no corresponde a ningún socio registrado.")
                context = {
                    'form': form,
                    'regions': Region.objects.all(),
                    'comunas': Comuna.objects.all(),
                    'es_edicion': False
                }
                return render(request, 'appsocios/empresa/crear_empresa.html', context)

            # Crear empresa asociada al socio encontrado
            empresa = form.save(commit=False)
            empresa.socio = socio
            empresa.save()

            # Guardar ID de la empresa en la sesión para la encuesta
            request.session['empresa_id'] = empresa.id_empresa

            # Pasar variable de éxito al template
            context = {
                'form': form,
                'regions': Region.objects.all(),
                'comunas': Comuna.objects.all(),
                'es_edicion': False,
                'empresa_creada': True,
                'empresa': empresa,
            }
            return render(request, 'appsocios/empresa/crear_empresa.html', context)
    else:
        form = EmpresaForm()

    context = {
        'form': form,
        'regions': Region.objects.all(),
        'comunas': Comuna.objects.all(),
        'es_edicion': False
    }
    return render(request, 'appsocios/empresa/crear_empresa.html', context)

def lista_empresas(request):
    import json
    empresas = Empresa.objects.all()
    rubros = Rubro.objects.all()

    # Convertir empresas a JSON para pasar a JavaScript
    empresas_data = []
    for emp in empresas:
        empresas_data.append({
            'id': emp.id_empresa,
            'nombre': emp.nombre,
            'rubro': emp.rubro.nombre_rubro if emp.rubro else 'Sin rubro',
            'telefono': emp.telefono or 'N/A',
            'correo': emp.correo or 'N/A',
            'direccion': emp.direccion_completa or emp.calle or 'N/A',
            'imagen': emp.foto.url if emp.foto else '/static/imagenes/default-empresa.jpg',
            'latitud': float(emp.latitud) if emp.latitud else -35.0,
            'longitud': float(emp.longitud) if emp.longitud else -71.2,
        })

    return render(request, 'appsocios/empresa/lista_empresas.html', {
        'empresas': empresas,
        'rubros': rubros,
        'empresas_json': json.dumps(empresas_data),
    })

def encuesta(request):
    empresa_id = request.session.get('empresa_id')
    
    if not empresa_id:
        messages.error(request, "⚠️ No hay empresa asociada. Por favor crea una empresa primero.")
        return redirect('appsocios:crear_empresa')
    
    try:
        empresa = Empresa.objects.get(id_empresa=empresa_id)
    except Empresa.DoesNotExist:
        messages.error(request, "⚠️ La empresa no existe.")
        return redirect('crear_empresa')
    
    # Obtener o crear la encuesta
    encuesta, created = Encuesta.objects.get_or_create(empresa=empresa)
    
    if request.method == 'POST':
        form = EncuestaForm(request.POST, instance=encuesta)
        if form.is_valid():
            form.save()
            # Limpiar la sesión
            if 'empresa_id' in request.session:
                del request.session['empresa_id']
            # Pasar variable de éxito al template
            context = {
                'form': form,
                'empresa': empresa,
                'encuesta_enviada': True,
            }
            return render(request, 'appsocios/socio/encuesta.html', context)
    else:
        form = EncuestaForm(instance=encuesta)
    
    context = {
        'form': form,
        'empresa': empresa,
    }
    return render(request, 'appsocios/socio/encuesta.html', context)

def editar_empresa(request, id_empresa):
    empresa = get_object_or_404(Empresa, id_empresa=id_empresa)
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, instance=empresa)
        if form.is_valid():
            form.save()
            messages.success(request, "")
            return redirect('appsocios:lista_empresas')
    else:
        form = EmpresaForm(instance=empresa)
    
    context = {
        'form': form,
        'regions': Region.objects.all(),
        'comunas': Comuna.objects.all(),
        'empresa': empresa,
        'es_edicion': True
    }
    return render(request, 'appsocios/empresa/crear_empresa.html', context)