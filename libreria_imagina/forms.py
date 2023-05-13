from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Field, ButtonHolder
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.validators import validate_email
from django import forms

from .models import Usuario, UsuarioManager


class LoginForm(AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data["username"]
        if "@" in username:  # Verificar si el campo es un email
            try:
                validate_email(username)
                return username
            except forms.ValidationError:
                raise forms.ValidationError("Ingrese un email válido.")
        return username

    def non_field_errors(self):
        return self.errors.get(
            "__all__", None
        )  # Retorna solo el mensaje de error general, sin ' * __all__ *'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Correo"
        self.fields["password"].label = "Contraseña"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field(
                "username",
                css_class="input-border form-control form-control-lg",
                placeholder="Correo",
            ),
            Field(
                "password",
                css_class="input-border form-control form-control-lg ",
                placeholder="Contraseña",
            ),
            ButtonHolder(
                Submit(
                    "submit",
                    "Iniciar Sesión",
                    css_class="btn btn-gradient w-100 d-block",
                )
            ),
        )


class SignupForm(forms.ModelForm):
    password1 = forms.CharField(label="Contraseña", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Confirmar Contraseña", widget=forms.PasswordInput
    )

    def clean_email(self):
        correo = self.cleaned_data["correo"]
        try:
            validate_email(correo)
            return correo
        except forms.ValidationError:
            raise forms.ValidationError("Ingrese un correo válido.")

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)
        if commit:
            user.save()
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["autofocus"] = True
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field(
                "username",
                css_class="input-border form-control form-control-lg",
                placeholder="Usuario",
            ),
            Field(
                "rut",
                css_class="input-border form-control form-control-lg",
                placeholder="RUT",
            ),
            Field(
                "nombre",
                css_class="input-border form-control form-control-lg",
                placeholder="Nombre",
            ),
            Field(
                "apellido",
                css_class="input-border form-control form-control-lg",
                placeholder="Apellido",
            ),
            Field(
                "correo",
                css_class="input-border form-control form-control-lg",
                placeholder="Correo",
            ),
            Field(
                "telefono",
                css_class="input-border form-control form-control-lg",
                placeholder="Teléfono",
            ),
            Field(
                "password1",
                css_class="input-border form-control form-control-lg",
                placeholder="Contraseña",
            ),
            Field(
                "password2",
                css_class="input-border form-control form-control-lg",
                placeholder="Confirmar Contraseña",
            ),
            ButtonHolder(
                Submit(
                    "submit",
                    "Registrarse",
                    css_class="btn btn-gradient w-100 d-block",
                    disabled="disabled",
                    css_id="submit-btn",
                )
            ),
        )

    class Meta:
        model = Usuario
        fields = (
            "username",
            "rut",
            "nombre",
            "apellido",
            "correo",
            "telefono",
        )

        error_messages = {
            "correo": {"invalid": "Ingrese un correo válido."},
            "password2": {"password_mismatch": "Las contraseñas no coinciden."},
        }
