from django.shortcuts import redirect, render
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from .forms import LoginForm
from crispy_forms.helper import FormHelper

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
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Redireccionar a la página deseada después del inicio de sesión exitoso
                return redirect('index')
    else:
        form = LoginForm(request)
    return render(request, "auth/login.html", {'form': form})


