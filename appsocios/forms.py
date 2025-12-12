from django import forms
from django.core.exceptions import ValidationError
from .models import Socio, Empresa, Rubro, TipoComercializacion, Encuesta

class SocioForm(forms.ModelForm):
    class Meta:
        model = Socio
        fields = [
            'socio_rut', 'socio_nombre', 'socio_apellido_paterno', 'socio_apellido_materno',
            'socio_celular', 'socio_fijo', 'socio_correo', 'socio_region', 'socio_direccion',
            'socio_numero', 'socio_comuna'
        ]

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

class RubroForm(forms.ModelForm):
    class Meta:
        model = Rubro
        fields = ['nombre_rubro']

class TipoComercializacionForm(forms.ModelForm):
    class Meta:
        model = TipoComercializacion
        fields = ['nombre_tipo']

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