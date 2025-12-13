from django.shortcuts import render, redirect, get_object_or_404
from .forms import SocioForm, RubroForm, TipoComercializacionForm, EmpresaForm, EncuestaForm, CambiarContrasenaForm
from .models import Socio, Empresa, Rubro, TipoComercializacion, Region, Comuna, Encuesta
from django.contrib import messages
from applogin.utils import es_admin, es_socio
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password

def empresas(request):
    return render(request, 'appsocios/empresas.html')

def crear_socio(request):
    if request.method == 'POST':
        form = SocioForm(request.POST)
        if form.is_valid():
            socio = form.save(commit=False)
            socio.socio_estado = "Activo"
            
            # Limpiar RUT: remover puntos y guiones para consistencia
            socio.socio_rut = socio.socio_rut.upper().replace('.', '').replace('-', '')
            
            # Guardar el socio (el formulario ya hashea la contraseña en su método save)
            socio.save()
            
            return redirect('appsocios:lista_empresas')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = SocioForm()
    return render(request, 'appsocios/socio/crear_socio.html', {'form': form})


def editar_socio(request):
    """Editar el perfil del socio logeado"""
    # Si es un socio logeado por sesión
    if 'socio_id' in request.session:
        socio = get_object_or_404(Socio, socio_id=request.session['socio_id'])
    # Si es un usuario con rol socio en Django
    elif es_socio(request.user):
        socio = get_object_or_404(Socio, usuario=request.user)
    else:
        
        return redirect('appsocios:lista_empresas')
    
    if request.method == 'POST':
        form = SocioForm(request.POST, instance=socio)
        if form.is_valid():
            socio_editado = form.save(commit=False)
            
            # Limpiar RUT: remover puntos y guiones para consistencia
            socio_editado.socio_rut = socio_editado.socio_rut.upper().replace('.', '').replace('-', '')
            
            # Guardar los cambios
            socio_editado.save()
            
            
            return redirect('appsocios:lista_empresas')
        else:
            messages.error(request, "Por favor corrige los errores del formulario.")
    else:
        form = SocioForm(instance=socio)
    
    return render(request, 'appsocios/socio/editar_socio.html', {
        'form': form,
        'socio': socio,
        'es_edicion': True
    })


def cambiar_contrasena(request):
    """Cambiar la contraseña del socio logeado"""
    # Si es un socio logeado por sesión
    if 'socio_id' in request.session:
        socio = get_object_or_404(Socio, socio_id=request.session['socio_id'])
    # Si es un usuario con rol socio en Django
    elif es_socio(request.user):
        socio = get_object_or_404(Socio, usuario=request.user)
    else:
        messages.error(request, "Debes ser un socio para cambiar tu contraseña.")
        return redirect('appsocios:lista_empresas')
    
    if request.method == 'POST':
        form = CambiarContrasenaForm(request.POST, socio=socio)
        if form.is_valid():
            contrasena_nueva = form.cleaned_data.get('contrasena_nueva')
            socio.socio_contraseña = make_password(contrasena_nueva)
            socio.save()
            return redirect('appsocios:lista_empresas')
    else:
        form = CambiarContrasenaForm(socio=socio)
    
    return render(request, 'appsocios/socio/cambiar_contrasena.html', {
        'form': form,
        'socio': socio
    })


def lista_rubros(request):
    rubros = Rubro.objects.all()
    return render(request, 'appsocios/empresa/lista_rubros.html', {'rubros': rubros})

def crear_rubro(request):
    if request.method == 'POST':
        form = RubroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Rubro creado exitosamente.")
            return redirect('appsocios:lista_rubros')
    else:
        form = RubroForm()
    return render(request, 'appsocios/empresa/crear_rubro.html', {'form': form})

def editar_rubro(request, id_rubro):
    rubro = get_object_or_404(Rubro, id_rubro=id_rubro)
    if request.method == 'POST':
        form = RubroForm(request.POST, instance=rubro)
        if form.is_valid():
            form.save()
            messages.success(request, "Rubro actualizado exitosamente.")
            return redirect('appsocios:lista_rubros')
    else:
        form = RubroForm(instance=rubro)
    return render(request, 'appsocios/empresa/crear_rubro.html', {'form': form, 'es_edicion': True})

def eliminar_rubro(request, id_rubro):
    rubro = get_object_or_404(Rubro, id_rubro=id_rubro)
    if request.method == 'POST':
        rubro.delete()
        messages.success(request, "Rubro eliminado exitosamente.")
        return redirect('appsocios:lista_rubros')
    return render(request, 'appsocios/empresa/eliminar_rubro.html', {'rubro': rubro})

def lista_tipos_comercializacion(request):
    tipos = TipoComercializacion.objects.all()
    return render(request, 'appsocios/empresa/lista_tipos_comercializacion.html', {'tipos': tipos})

def crear_tipo_comercializacion(request):
    if request.method == 'POST':
        form = TipoComercializacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de comercialización creado exitosamente.")
            return redirect('appsocios:lista_tipos_comercializacion')
    else:
        form = TipoComercializacionForm()
    return render(request, 'appsocios/empresa/crear_tipo_comercializacion.html', {'form': form})

def editar_tipo_comercializacion(request, id_tipo):
    tipo = get_object_or_404(TipoComercializacion, id_tipo=id_tipo)
    if request.method == 'POST':
        form = TipoComercializacionForm(request.POST, instance=tipo)
        if form.is_valid():
            form.save()
            messages.success(request, "Tipo de comercialización actualizado exitosamente.")
            return redirect('appsocios:lista_tipos_comercializacion')
    else:
        form = TipoComercializacionForm(instance=tipo)
    return render(request, 'appsocios/empresa/crear_tipo_comercializacion.html', {'form': form, 'es_edicion': True})

def eliminar_tipo_comercializacion(request, id_tipo):
    tipo = get_object_or_404(TipoComercializacion, id_tipo=id_tipo)
    if request.method == 'POST':
        tipo.delete()
        messages.success(request, "Tipo de comercialización eliminado exitosamente.")
        return redirect('appsocios:lista_tipos_comercializacion')
    return render(request, 'appsocios/empresa/eliminar_tipo_comercializacion.html', {'tipo': tipo})

def crear_empresa(request):
    # Verificar que el usuario sea admin o socio
    if not es_admin(request.user) and not es_socio(request.user, request):
        messages.error(request, "No tienes permiso para crear empresas.")
        return redirect('appsocios:lista_empresas')
    
    es_usuario_socio = es_socio(request.user, request)
    es_usuario_admin = es_admin(request.user)
    
    if request.method == 'POST':
        form = EmpresaForm(request.POST, request.FILES, es_socio=es_usuario_socio)
        if form.is_valid():
            # Si es socio, obtener su socio vinculado
            if es_usuario_socio:
                try:
                    # Si es socio loggeado por sesión, usar el socio_id de la sesión
                    if request.session.get('es_socio_login'):
                        socio = Socio.objects.get(socio_id=request.session.get('socio_id'))
                    else:
                        # Si es socio vinculado a usuario Django
                        socio = Socio.objects.get(usuario=request.user)
                except Socio.DoesNotExist:
                    messages.error(request, " No tienes un perfil de socio vinculado.")
                    context = {
                        'form': form,
                        'regions': Region.objects.all(),
                        'comunas': Comuna.objects.all(),
                        'es_edicion': False,
                        'es_socio': True,
                        'es_admin': es_usuario_admin
                    }
                    return render(request, 'appsocios/empresa/crear_empresa.html', context)
            elif es_usuario_admin:
                # Si es admin, buscar por RUN ingresado
                run_socio = form.cleaned_data.get('run_socio')

                # Validar que run_socio no sea vacío en creación
                if not run_socio:
                    messages.error(request, " Debes ingresar el RUN del socio.")
                    context = {
                        'form': form,
                        'regions': Region.objects.all(),
                        'comunas': Comuna.objects.all(),
                        'es_edicion': False,
                        'es_socio': False,
                        'es_admin': True
                    }
                    return render(request, 'appsocios/empresa/crear_empresa.html', context)

                # Buscar socio por RUN
                try:
                    socio = Socio.objects.get(socio_rut=run_socio)
                except Socio.DoesNotExist:
                    messages.error(request, " El RUN ingresado no corresponde a ningún socio registrado.")
                    context = {
                        'form': form,
                        'regions': Region.objects.all(),
                        'comunas': Comuna.objects.all(),
                        'es_edicion': False,
                        'es_socio': False,
                        'es_admin': True
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
                'es_socio': es_usuario_socio,
                'es_admin': es_usuario_admin
            }
            return render(request, 'appsocios/empresa/crear_empresa.html', context)
    else:
        form = EmpresaForm(es_socio=es_usuario_socio)

    context = {
        'form': form,
        'regions': Region.objects.all(),
        'comunas': Comuna.objects.all(),
        'es_edicion': False,
        'es_socio': es_usuario_socio,
        'es_admin': es_usuario_admin
    }
    return render(request, 'appsocios/empresa/crear_empresa.html', context)

def lista_empresas(request):
    import json
    
    rubro_seleccionado = request.GET.get('rubro')
    empresas = Empresa.objects.all()

    if rubro_seleccionado:
        empresas = empresas.filter(rubro__id_rubro=rubro_seleccionado)

    rubros = Rubro.objects.all()

    # Convertir empresas a JSON para pasar a JavaScript
    empresas_data = []
    for emp in empresas:
        empresas_data.append({
            'id': emp.id_empresa,
            'nombre': emp.nombre,
            'rubro': emp.rubro.nombre_rubro if emp.rubro else 'Sin rubro',
            'rubro_id': emp.rubro.id_rubro if emp.rubro else '',
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
        'rubro_seleccionado': rubro_seleccionado,
        'empresas_json': json.dumps(empresas_data),
        'es_admin': es_admin(request.user),
        'es_socio': es_socio(request.user, request),
    })

def encuesta(request):
    empresa_id = request.session.get('empresa_id')
    
    if not empresa_id:
        messages.error(request, " No hay empresa asociada. Por favor crea una empresa primero.")
        return redirect('appsocios:crear_empresa')
    
    try:
        empresa = Empresa.objects.get(id_empresa=empresa_id)
    except Empresa.DoesNotExist:
        messages.error(request, " La empresa no existe.")
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


def login_socio(request):
    """Vista de login para socios"""
    from .forms_login import SocioLoginForm
    
    if request.method == 'POST':
        form = SocioLoginForm(request.POST)
        if form.is_valid():
            rut = form.cleaned_data.get('rut').upper().replace('.', '').replace('-', '')
            contraseña = form.cleaned_data.get('contraseña')
            
            try:
                # Buscar socio por RUT
                socio = Socio.objects.get(socio_rut=rut)
                
                # Verificar contraseña
                if socio.socio_contraseña and check_password(contraseña, socio.socio_contraseña):
                    # Crear sesión para el socio
                    request.session['socio_id'] = socio.socio_id
                    request.session['socio_nombre'] = f"{socio.socio_nombre} {socio.socio_apellido_paterno}"
                    request.session['socio_rut'] = socio.socio_rut
                    
                    
                    return redirect('appsocios:lista_empresas')
                else:
                    messages.error(request, "RUT o contraseña incorrectos.")
            except Socio.DoesNotExist:
                messages.error(request, "RUT o contraseña incorrectos.")
    else:
        form = SocioLoginForm()
    
    return render(request, 'appsocios/socio/login_socio.html', {'form': form})