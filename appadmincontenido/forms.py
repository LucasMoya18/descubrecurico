from django import forms
from .models import Evento, Articulo, BloqueArticulo, Comentario, Categoria, Actividad, Noticia, Reportaje, BloqueNoticia, BloqueReportaje
from django.forms import inlineformset_factory
from django.utils import timezone

BASE_INPUT = {"class": "w-full px-3 py-2 rounded-lg border"}
BASE_TEXTAREA = {"class": "w-full px-3 py-2 rounded-lg border", "rows": "3"}
BASE_SELECT = {"class": "w-full px-3 py-2 rounded-lg border"}
BASE_FILE = {"class": "w-full px-3 py-2 rounded-lg border"}

BASE_INPUT_STYLE = "w-full px-4 py-3 rounded border border-gray-200 placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition duration-200"

class EventoActividadForm(forms.ModelForm):
    def __init__(self, *args, tipo=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Ajustar el formato de fecha para los inputs datetime-local al editar
        if self.instance and self.instance.pk:
            if self.instance.fecha_inicio:
                # Convertir a la zona horaria local antes de formatear
                local_inicio = timezone.localtime(self.instance.fecha_inicio)
                self.initial['fecha_inicio'] = local_inicio.strftime('%Y-%m-%dT%H:%M')
            if self.instance.fecha_termino:
                # Convertir a la zona horaria local antes de formatear
                local_termino = timezone.localtime(self.instance.fecha_termino)
                self.initial['fecha_termino'] = local_termino.strftime('%Y-%m-%dT%H:%M')
        
        # Lógica para personalizar placeholders según si es Evento o Actividad
        texto_titulo = "Título del evento" if tipo == "evento" else "Título de la actividad"
        texto_desc = "Descripción del evento" if tipo == "evento" else "Descripción de la actividad"
        texto_lugar = "Lugar del evento" if tipo == "evento" else "Lugar de la actividad"

        self.fields['titulo'].widget.attrs['placeholder'] = texto_titulo
        self.fields['descripcion'].widget.attrs['placeholder'] = texto_desc
        self.fields['lugar'].widget.attrs['placeholder'] = texto_lugar

    class Meta:
        model = Evento  
        fields = ["titulo", "descripcion", "fecha_inicio", "fecha_termino", "lugar"]
        
        widgets = {
            "titulo": forms.TextInput(attrs={
                "class": BASE_INPUT_STYLE
            }),
            "descripcion": forms.Textarea(attrs={
                "class": BASE_INPUT_STYLE, 
                "rows": "3" # Altura similar a la foto
            }),
            "lugar": forms.TextInput(attrs={
                "class": BASE_INPUT_STYLE
            }),
            # Los inputs de fecha en la foto tienen un estilo similar
            "fecha_inicio": forms.DateTimeInput(attrs={
                "class": BASE_INPUT_STYLE,
                "type": "datetime-local" 
            }),
            "fecha_termino": forms.DateTimeInput(attrs={
                "class": BASE_INPUT_STYLE,
                "type": "datetime-local"
            }),
        }

# --- ARTÍCULO ---
class ArticuloForm(forms.ModelForm):
    nuevas_categorias = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Crear nuevas (separadas por coma)"}),
        label="Nuevas categorías"
    )
    categorias = forms.ModelMultipleChoiceField(
        queryset=Categoria.objects.all().order_by("nombre"),
        required=False,
        widget=forms.SelectMultiple(attrs={**BASE_SELECT, "size": "6"}),
        label="Categorías existentes"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Si estamos editando (hay una instancia), pre-populamos las categorías
        if self.instance and self.instance.pk:
            self.fields['categorias'].initial = self.instance.categorias.all()


    class Meta:
        model = Articulo
        fields = ["titulo", "resumen", "autor", "categorias", "nuevas_categorias", "portada", "estado"]
        widgets = {
            "titulo": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Título"}),
            "resumen": forms.Textarea(attrs={**BASE_TEXTAREA, "placeholder": "Resumen"}),
            "autor": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Autor"}),
            "portada": forms.ClearableFileInput(attrs=BASE_FILE),
            "estado": forms.Select(attrs=BASE_SELECT),
        }
    
    def save(self, commit=True):
        # Guardamos el artículo principal
        instance = super().save(commit=False)

        # Procesamos las nuevas categorías
        nuevas_categorias_str = self.cleaned_data.get('nuevas_categorias', '')
        if nuevas_categorias_str:
            nombres_nuevas = [name.strip() for name in nuevas_categorias_str.split(',') if name.strip()]
            for nombre in nombres_nuevas:
                # Usamos get_or_create para evitar duplicados y obtener la categoría
                categoria, created = Categoria.objects.get_or_create(nombre=nombre)
                # La añadimos a las categorías seleccionadas del formulario
                self.cleaned_data['categorias'] = self.cleaned_data['categorias'].union(Categoria.objects.filter(pk=categoria.pk))

        # Si commit es True, guardamos la instancia y las relaciones M2M
        if commit:
            instance.save()
            self.save_m2m() # Esto guardará las 'categorias'
        return instance

# --- FORMULARIOS DE BLOQUES ---
class BloqueArticuloForm(forms.ModelForm):
    class Meta:
        model = BloqueArticulo
        fields = ["orden", "tipo", "subtitulo", "texto", "imagen", "pie_de_foto", "estilo_imagen", "url"]
        widgets = {
            "orden": forms.NumberInput(attrs={**BASE_INPUT, "class": "orden-field hidden"}),
            "tipo": forms.Select(attrs=BASE_SELECT),
            "subtitulo": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Subtítulo"}),
            "texto": forms.Textarea(attrs={**BASE_TEXTAREA, "placeholder": "Texto"}),
            "imagen": forms.ClearableFileInput(attrs=BASE_FILE),
            "pie_de_foto": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Pie de foto"}),
            "estilo_imagen": forms.Select(attrs=BASE_SELECT),
            "url": forms.URLInput(attrs={**BASE_INPUT, "placeholder": "URL / YouTube / MP4"}),
        }

class BloqueNoticiaForm(forms.ModelForm):
    class Meta:
        model = BloqueNoticia
        fields = ["orden", "tipo", "subtitulo", "texto", "imagen", "pie_de_foto", "estilo_imagen", "url"]
        widgets = {
            "orden": forms.NumberInput(attrs={**BASE_INPUT, "class": "orden-field hidden"}),
            "tipo": forms.Select(attrs=BASE_SELECT),
            "subtitulo": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Subtítulo"}),
            "texto": forms.Textarea(attrs={**BASE_TEXTAREA, "placeholder": "Texto"}),
            "imagen": forms.ClearableFileInput(attrs=BASE_FILE),
            "pie_de_foto": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Pie de foto"}),
            "estilo_imagen": forms.Select(attrs=BASE_SELECT),
            "url": forms.URLInput(attrs={**BASE_INPUT, "placeholder": "URL / YouTube / MP4"}),
        }

class BloqueReportajeForm(forms.ModelForm):
    class Meta:
        model = BloqueReportaje
        fields = ["orden", "tipo", "subtitulo", "texto", "imagen", "pie_de_foto", "estilo_imagen", "url"]
        widgets = {
            "orden": forms.NumberInput(attrs={**BASE_INPUT, "class": "orden-field hidden"}),
            "tipo": forms.Select(attrs=BASE_SELECT),
            "subtitulo": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Subtítulo"}),
            "texto": forms.Textarea(attrs={**BASE_TEXTAREA, "placeholder": "Texto"}),
            "imagen": forms.ClearableFileInput(attrs=BASE_FILE),
            "pie_de_foto": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Pie de foto"}),
            "estilo_imagen": forms.Select(attrs=BASE_SELECT),
            "url": forms.URLInput(attrs={**BASE_INPUT, "placeholder": "URL / YouTube / MP4"}),
        }

# --- FORMSETS ---
BloqueArticuloFormSet = inlineformset_factory(
    Articulo,
    BloqueArticulo,
    form=BloqueArticuloForm,
    extra=0,
    can_delete=True,
)

BloqueNoticiaFormSet = inlineformset_factory(
    Noticia,
    BloqueNoticia,
    form=BloqueNoticiaForm,
    extra=0,
    can_delete=True,
)

BloqueReportajeFormSet = inlineformset_factory(
    Reportaje,
    BloqueReportaje,
    form=BloqueReportajeForm,
    extra=0,
    can_delete=True,
)

# Alias para compatibilidad
BloqueFormSet = BloqueArticuloFormSet
ComentarioForm = forms.ModelForm

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ["nombre", "email", "texto"]
        widgets = {
            "nombre": forms.TextInput(attrs={**BASE_INPUT, "placeholder": "Nombre"}),
            "email": forms.EmailInput(attrs={**BASE_INPUT, "placeholder": "Email"}),
            "texto": forms.Textarea(attrs={**BASE_TEXTAREA, "rows": "4", "placeholder": "Tu comentario"}),
        }