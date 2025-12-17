from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from applogin.decorators import solo_admin, solo_socio
from .models import Evento, Articulo, Categoria, Actividad, Noticia, Reportaje, BloqueArticulo, BloqueNoticia, BloqueReportaje
from .forms import (
    ArticuloForm, 
    BloqueArticuloFormSet, 
    BloqueNoticiaFormSet, 
    BloqueReportajeFormSet,
    ComentarioForm, 
    EventoActividadForm
)
from django.utils import timezone
from django.utils.text import slugify

def articulos(request):
    articulos_qs = Articulo.objects.prefetch_related("categorias")
    noticias_qs = Noticia.objects.prefetch_related("categorias")
    reportajes_qs = Reportaje.objects.prefetch_related("categorias")
    
    todos = list(articulos_qs) + list(noticias_qs) + list(reportajes_qs)
    
    tipo_filter = request.GET.get('tipo', '')
    if tipo_filter == 'articulo':
        todos = [a for a in todos if a.__class__.__name__ == 'Articulo']
    elif tipo_filter == 'noticia':
        todos = [a for a in todos if a.__class__.__name__ == 'Noticia']
    elif tipo_filter == 'reportaje':
        todos = [a for a in todos if a.__class__.__name__ == 'Reportaje']
    
    categoria_filter = request.GET.get('categoria', '')
    if categoria_filter:
        todos = [a for a in todos if a.categorias.filter(slug=categoria_filter).exists()]
    
    todos.sort(key=lambda x: x.publicado_en, reverse=True)
    
    paginator = Paginator(todos, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    
    categorias = Categoria.objects.all().order_by("nombre")
    
    return render(request, 'appadmincontenido/articulos.html', {
        "page_obj": page_obj,
        "categorias": categorias,
        "tipo_filter": tipo_filter,
        "categoria_filter": categoria_filter,
    })

def articulo_detalle(request, slug):
    articulo = get_object_or_404(
        Articulo.objects.prefetch_related("categorias", "bloques", "comentarios"),
        slug=slug
    )
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.content_object = articulo
            c.save()
            messages.success(request, "Comentario enviado.")
            return redirect(articulo.get_absolute_url())
    else:
        form = ComentarioForm()
    return render(request, "appadmincontenido/articulo_detalle.html", {"articulo": articulo, "form": form})

def noticia_detalle(request, slug):
    noticia = get_object_or_404(
        Noticia.objects.prefetch_related("categorias", "bloques"),
        slug=slug
    )
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.content_object = noticia
            c.save()
            messages.success(request, "Comentario enviado.")
            return redirect(noticia.get_absolute_url())
    else:
        form = ComentarioForm()
    return render(request, "appadmincontenido/articulo_detalle.html", {"articulo": noticia, "form": form})

def reportaje_detalle(request, slug):
    reportaje = get_object_or_404(
        Reportaje.objects.prefetch_related("categorias", "bloques"),
        slug=slug
    )
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            c = form.save(commit=False)
            c.content_object = reportaje
            c.save()
            messages.success(request, "Comentario enviado.")
            return redirect(reportaje.get_absolute_url())
    else:
        form = ComentarioForm()
    return render(request, "appadmincontenido/articulo_detalle.html", {"articulo": reportaje, "form": form})

def _get_formset_for_tipo(tipo):
    """Retorna el formset correcto según el tipo"""
    formset_map = {
        "articulo": BloqueArticuloFormSet,
        "noticia": BloqueNoticiaFormSet,
        "reportaje": BloqueReportajeFormSet,
    }
    return formset_map.get(tipo, BloqueArticuloFormSet)

@solo_admin
def articulo_crear(request, tipo):
    model_map = {
        "articulo": Articulo,
        "noticia": Noticia,
        "reportaje": Reportaje,
    }
    model = model_map.get(tipo)
    if not model:
        return redirect("appadmincontenido:articulos")
    
    FormSet = _get_formset_for_tipo(tipo)
    
    if request.method == "POST":
        form = ArticuloForm(request.POST, request.FILES)
        formset = FormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            # El nuevo form.save() maneja las categorías
            obj = form.save(commit=False) 
            obj.__class__ = model
            obj.save() # Guardamos el objeto con la clase correcta
            form.save_m2m() # Guardamos las relaciones
            formset.instance = obj
            formset.save()
            messages.success(request, f"{tipo.capitalize()} creado exitosamente.")
            return redirect(obj.get_absolute_url())
    else:
        form = ArticuloForm()
        formset = FormSet()
    
    return render(request, "appadmincontenido/articulo_form.html", {
        "form": form,
        "formset": formset,
        "tipo": tipo.capitalize()
    })


@solo_admin
def articulo_editar(request, slug, tipo):
    model_map = {
        "articulo": Articulo,
        "noticia": Noticia,
        "reportaje": Reportaje,
    }
    model = model_map.get(tipo)
    if not model:
        return redirect("appadmincontenido:articulos")
    
    obj = get_object_or_404(model, slug=slug)
    FormSet = _get_formset_for_tipo(tipo)
    
    if request.method == "POST":
        form = ArticuloForm(request.POST, request.FILES, instance=obj)
        formset = FormSet(request.POST, request.FILES, instance=obj)
        
        if form.is_valid() and formset.is_valid():
            # Guardar el objeto sin cambiar clase
            updated_obj = form.save() # El form.save() ahora se encarga de todo
            formset.save()
            
            messages.success(request, f"{tipo.capitalize()} actualizado exitosamente.")
            return redirect(updated_obj.get_absolute_url())
        else:
            if form.errors:
                messages.error(request, f"Errores en el formulario: {form.errors}")
            if formset.errors:
                messages.error(request, f"Errores en bloques: {formset.errors}")
    else:
        form = ArticuloForm(instance=obj)
        formset = FormSet(instance=obj)
    
    return render(request, "appadmincontenido/articulo_form.html", {
        "form": form,
        "formset": formset,
        "tipo": tipo.capitalize(),
        "es_edicion": True,
    })

@solo_admin
def articulo_eliminar(request, slug, tipo):
    model_map = {
        "articulo": Articulo,
        "noticia": Noticia,
        "reportaje": Reportaje,
    }
    model = model_map.get(tipo)
    if not model:
        return redirect("appadmincontenido:articulos")
    
    obj = get_object_or_404(model, slug=slug)
    
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"{tipo.capitalize()} eliminado exitosamente.")
        return redirect("appadmincontenido:articulos")
    
    return render(request, "appadmincontenido/articulo_confirmar_eliminar.html", {
        "objeto": obj,
        "tipo": tipo.capitalize(),
    })

def eventos(request):
    now = timezone.now()
    
    # Obtener todos los eventos y actividades para las listas
    eventos_todos = Evento.objects.all().order_by("fecha_inicio")
    actividades_todas = Actividad.objects.all().order_by("fecha_inicio")

    # Encontrar el próximo evento o actividad
    eventos_futuros = eventos_todos.filter(fecha_inicio__gte=now)
    actividades_futuras = actividades_todas.filter(fecha_inicio__gte=now)
    
    todos_futuros = sorted(list(eventos_futuros) + list(actividades_futuras), key=lambda x: x.fecha_inicio)
    
    proximo_item = todos_futuros[0] if todos_futuros else None
    siguiente_item = todos_futuros[1] if len(todos_futuros) > 1 else None

    return render(request, 'appadmincontenido/eventos.html', {
        "eventos": eventos_todos,
        "actividades": actividades_todas,
        "proximo_item": proximo_item,
        "siguiente_item": siguiente_item,
    })

@solo_admin
def evento_crear(request):
    if request.method == "POST":
        form = EventoActividadForm(request.POST, tipo="evento")
        if form.is_valid():
            evento = form.save(commit=False)
            if not evento.slug:
                evento.slug = slugify(evento.titulo)[:50]  # ajustar longitud si aplica
            evento.__class__ = Evento
            evento.save()
            messages.success(request, "Evento creado exitosamente.")
            return redirect("appadmincontenido:eventos")
    else:
        form = EventoActividadForm(tipo="evento")

    return render(request, "appadmincontenido/actividad_form.html", {
        "form": form,
        "accion": "Crear Evento"
    })

@solo_admin
def actividad_crear(request):
    if request.method == "POST":
        form = EventoActividadForm(request.POST, tipo="actividad")
        if form.is_valid():
            actividad = form.save(commit=False)
            if not actividad.slug:
                actividad.slug = slugify(actividad.titulo)[:50]
            actividad.__class__ = Actividad
            actividad.save()
            messages.success(request, "Actividad creada exitosamente.")
            return redirect("appadmincontenido:eventos")
    else:
        form = EventoActividadForm(tipo="actividad")
    
    return render(request, "appadmincontenido/actividad_form.html", {
        "form": form,
        "accion": "Crear Actividad"
    })

@solo_admin
def evento_editar(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    if request.method == "POST":
        form = EventoActividadForm(request.POST, instance=evento, tipo="evento")
        if form.is_valid():
            evento = form.save(commit=False)
            if not evento.slug:
                evento.slug = slugify(evento.titulo)[:50]
            evento.save()
            messages.success(request, "Evento actualizado exitosamente.")
            return redirect("appadmincontenido:eventos")
    else:
        form = EventoActividadForm(instance=evento, tipo="evento")
    return render(request, "appadmincontenido/actividad_form.html", {
        "form": form,
        "accion": "Editar Evento",
        "es_edicion": True
    })

@solo_admin
def evento_eliminar(request, slug):
    evento = get_object_or_404(Evento, slug=slug)
    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento eliminado exitosamente.")
        return redirect("appadmincontenido:eventos")
    return render(request, "appadmincontenido/actividad_confirmar_eliminar.html", {
        "actividad": evento,
        "accion": "Eliminar Evento"
    })

@solo_admin
def actividad_editar(request, slug):
    actividad = get_object_or_404(Actividad, slug=slug)
    if request.method == "POST":
        form = EventoActividadForm(request.POST, instance=actividad, tipo="actividad")
        if form.is_valid():
            actividad = form.save(commit=False)
            if not actividad.slug:
                actividad.slug = slugify(actividad.titulo)[:50]
            actividad.save()
            messages.success(request, "Actividad actualizada exitosamente.")
            return redirect("appadmincontenido:eventos")
    else:
        form = EventoActividadForm(instance=actividad, tipo="actividad")
    return render(request, "appadmincontenido/actividad_form.html", {
        "form": form,
        "accion": "Editar Actividad",
        "es_edicion": True
    })

@solo_admin
def actividad_eliminar(request, slug):
    actividad = get_object_or_404(Actividad, slug=slug)
    if request.method == "POST":
        actividad.delete()
        messages.success(request, "Actividad eliminada exitosamente.")
        return redirect("appadmincontenido:eventos")
    return render(request, "appadmincontenido/actividad_confirmar_eliminar.html", {
        "actividad": actividad,
        "accion": "Eliminar Actividad"
    })
