from django.contrib.auth.hashers import make_password, check_password

from django import forms
from django.core.exceptions import ValidationError
from .models import Socio, Empresa, Rubro, TipoComercializacion, Encuesta

class SocioForm(forms.ModelForm):
    socio_contraseña = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(),
        help_text="Ingresa tu contraseña para poder ingresar con tu perfil. Tu usuario será tu RUT.",
        required=True
        
    )
        
    
    class Meta:
        model = Socio
        fields = [
            'socio_rut', 'socio_nombre', 'socio_apellido_paterno', 'socio_apellido_materno',
            'socio_celular', 'socio_fijo', 'socio_correo', 'socio_region', 'socio_direccion',
            'socio_numero', 'socio_comuna'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # En creación, mostrar el campo de contraseña
        if not (self.instance and self.instance.pk):
            self.fields['socio_contraseña'].widget = forms.PasswordInput()
        else:
            # En edición, remover el campo de contraseña
            self.fields.pop('socio_contraseña', None)

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-burgundy-reserve focus:ring-2 focus:ring-burgundy-reserve/20',
                'placeholder': self.fields[field_name].label
            })
        
    def save(self, commit=True):
        # Obtener la contraseña antes de que sea procesada
        contraseña = self.cleaned_data.get('socio_contraseña')
        
        # Llamar al save del parent pero sin commit
        socio = super().save(commit=False)
        
        # Si hay contraseña y no es la contraseña hasheada anterior, hashearla
        # Detectar si es una contraseña hasheada (comienza con pbkdf2_sha256$)
        if contraseña and not contraseña.startswith('pbkdf2_sha256$'):
            socio.socio_contraseña = make_password(contraseña)
        # Si la contraseña parece hasheada, mantenerla como está
        
        if commit:
            socio.save()
        
        return socio


class CambiarContrasenaForm(forms.Form):
    contrasena_actual = forms.CharField(
        label="Contraseña Actual",
        widget=forms.PasswordInput(),
        help_text="Ingresa tu contraseña actual para verificación.",
        required=True
    )
    contrasena_nueva = forms.CharField(
        label="Contraseña Nueva",
        widget=forms.PasswordInput(),
        help_text="Ingresa tu nueva contraseña.",
        required=True
    )
    contrasena_nueva_confirmacion = forms.CharField(
        label="Confirmar Contraseña Nueva",
        widget=forms.PasswordInput(),
        help_text="Confirma tu nueva contraseña.",
        required=True
    )
    
    def __init__(self, *args, socio=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.socio = socio
        
        # Aplicar estilos a todos los campos
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-burgundy-reserve focus:ring-2 focus:ring-burgundy-reserve/20',
                'placeholder': self.fields[field_name].label
            })
    
    def clean(self):
        cleaned_data = super().clean()
        contrasena_actual = cleaned_data.get('contrasena_actual')
        contrasena_nueva = cleaned_data.get('contrasena_nueva')
        contrasena_nueva_confirmacion = cleaned_data.get('contrasena_nueva_confirmacion')
        
        # Verificar que la contraseña actual sea correcta
        if contrasena_actual and self.socio:
            if not check_password(contrasena_actual, self.socio.socio_contraseña):
                raise ValidationError("La contraseña actual no es correcta.")
        
        # Verificar que las contraseñas nuevas coincidan
        if contrasena_nueva and contrasena_nueva_confirmacion:
            if contrasena_nueva != contrasena_nueva_confirmacion:
                raise ValidationError("Las contraseñas nuevas no coinciden.")
        
        return cleaned_data

class EmpresaForm(forms.ModelForm):
    run_socio = forms.CharField(
        label="RUN del socio",
        max_length=12,
        required=False,
        help_text="Ingresa el RUN del socio que registrará esta empresa (solo en creación)."
    )

    class Meta:
        model = Empresa
        fields = [
            'nombre',
            'rut',  # <-- este sigue siendo el RUT de la empresa
            'direccion_completa',
            'calle',
            'comuna',
            'telefono',
            'correo',
            'instagram',
            'facebook',
            'web',
            'foto',
            'latitud',
            'longitud',
            'rubro',
            'tipo_comercializacion'
        ]
    
    def __init__(self, *args, es_socio=False, **kwargs):
        super().__init__(*args, **kwargs)
        # Si el usuario es socio, ocultar el campo run_socio
        if es_socio:
            self.fields['run_socio'].widget = forms.HiddenInput()
            self.fields['run_socio'].required = False
        
        # Agregar campos de región y comuna
        from .models import Region, Comuna
        self.fields['region'] = forms.ModelChoiceField(
            queryset=Region.objects.all(),
            required=False,
            label="Región",
            empty_label="-- Selecciona una región --"
        )
        self.fields['comuna'] = forms.ModelChoiceField(
            queryset=Comuna.objects.all(),
            required=False,
            label="Comuna",
            empty_label="-- Selecciona una comuna --"
        )
        
        # Setear valores iniciales si hay instance
        if self.instance and self.instance.pk and self.instance.comuna:
            self.fields['region'].initial = self.instance.comuna.provincia.region
            self.fields['comuna'].initial = self.instance.comuna
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.comuna = self.cleaned_data.get('comuna')
        if commit:
            instance.save()
        return instance

class RubroForm(forms.ModelForm):
    class Meta:
        model = Rubro
        fields = ['nombre_rubro']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_rubro'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-burgundy-reserve focus:ring-2 focus:ring-burgundy-reserve/20',
            'placeholder': 'Nombre del rubro'
        })

class TipoComercializacionForm(forms.ModelForm):
    class Meta:
        model = TipoComercializacion
        fields = ['nombre_tipo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre_tipo'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-burgundy-reserve focus:ring-2 focus:ring-burgundy-reserve/20',
            'placeholder': 'Nombre del tipo de comercialización'
        })

class EncuestaForm(forms.ModelForm):
    pregunta_1_descuento_comercializacion = forms.ChoiceField(
        choices=[('si', 'Sí'), ('no', 'No')],
        widget=forms.RadioSelect,
        required=True,
        label='¿Ofrece descuento por comercialización?'
    )
    
    class Meta:
        model = Encuesta
        fields = [
            'pregunta_1_descuento_comercializacion',
            'pregunta_2_tipo_descuento',
            'pregunta_2_porcentaje',
            'pregunta_3_valor_empresa',
            'pregunta_4_empresa_referencia',
            # pregunta_6_empresas_apoyan removed
        ]
        widgets = {
            'pregunta_3_valor_empresa': forms.Textarea(attrs={'rows': 3}),
            'pregunta_4_empresa_referencia': forms.TextInput(attrs={'placeholder': '¿Qué empresa te referencia? (nombre de la empresa)'}),
            'pregunta_2_porcentaje': forms.NumberInput(attrs={'min': 0, 'max': 100, 'step': 1, 'placeholder': '%'}),
            'pregunta_2_tipo_descuento': forms.TextInput(attrs={'placeholder': 'Describe el tipo de descuento (ej: 10% para socios, 2x1, etc.)'})
        }

    def clean(self):
        cleaned = super().clean()
        errores = {}

        # exigir respuesta a pregunta 1
        p1 = cleaned.get('pregunta_1_descuento_comercializacion')
        if not p1:
            self.add_error('pregunta_1_descuento_comercializacion', 'Debes responder esta pregunta.')

        # si responde 'si', exigir tipo y porcentaje
        if p1 and str(p1).lower() == 'si':
            tipo = cleaned.get('pregunta_2_tipo_descuento')
            porcentaje = cleaned.get('pregunta_2_porcentaje')
            if not tipo or not str(tipo).strip():
                self.add_error('pregunta_2_tipo_descuento', 'Debes describir el tipo de descuento si respondiste Sí.')
            if porcentaje is None:
                self.add_error('pregunta_2_porcentaje', 'Debes indicar el porcentaje de descuento.')

        # exigir que las preguntas abiertas no queden vacías
        for field in ['pregunta_3_valor_empresa', 'pregunta_4_empresa_referencia']:
            val = cleaned.get(field)
            if val is None or (isinstance(val, str) and not val.strip()):
                self.add_error(field, 'Este campo no puede quedar vacío.')

        return cleaned