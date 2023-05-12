from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, ButtonHolder
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email
from django import forms


class LoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data['username']
        if '@' in username:  # Verificar si el campo es un email
            try:
                validate_email(username)
                return username
            except forms.ValidationError:
                raise forms.ValidationError('Ingrese un email válido.')
        return username

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Correo" 
        self.fields['password'].label = "Contraseña" 
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('username', css_class='input-border form-control form-control-lg', placeholder='Correo'),
            Field('password', css_class='input-border form-control form-control-lg ', placeholder='Contraseña'),
            ButtonHolder(
                Submit('submit', 'Iniciar Sesión', css_class='btn btn-gradient w-100 d-block')
            )
        )
