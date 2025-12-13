from django import forms
from django.contrib.auth.hashers import check_password


class SocioLoginForm(forms.Form):
    rut = forms.CharField(
        label="RUT",
        max_length=12,
        widget=forms.TextInput(attrs={
            'placeholder': '12345678-9',
            'autocomplete': 'off'
        })
    )
    contraseña = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingresa tu contraseña'
        })
    )
