from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from .models import *
from django.utils.html import escapejs

from .forms import SignupForm


# Create your views here.
def index(request):
    # Se obtienen 10 libros aleatorios de la base de datos
    libros = list(Libro.objects.order_by("nombre_libro", "fecha_publicacion")[:10])
    for libro in libros:
        libro.precio_unitario = format(libro.precio_unitario, ",.0f")
    # Se crea un diccionario con los libros obtenidos para pasarlo al contexto
    context = {"libros": libros}
    # Se renderiza la plantilla 'index.html' con el contexto creado
    return render(request, "app/index.html", context)


"""
AUTH

"""


def login_view(request):
    if request.user.is_authenticated:
        return redirect("index")  # Redirige al usuario autenticado a la página 'index'
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
        else:
            errors = form.errors.get("__all__", None)
            if errors:
                errors = [escapejs(error) for error in errors]
            return render(request, "auth/login.html", {"form": form, "errors": errors})
    else:
        form = AuthenticationForm(request)
    return render(request, "auth/login.html", {"form": form, "errors": ""})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect("index")  # Redirige al usuario autenticado a la página 'index'
    form = SignupForm()  # Crea una instancia del formulario SignupForm

    if request.method == "POST":
        # Procesa los datos del formulario si se envió una solicitud POST
        form = SignupForm(request.POST)
        if form.is_valid():
            # Realiza las acciones correspondientes al registro del usuario
            form.save()
            return HttpResponseRedirect(
                reverse("index")
            )  # Redireccionar a la página de registro exitoso

    # Renderiza la plantilla 'signup.html' con el formulario como contexto
    return render(request, "auth/signup.html", {"form": form})
