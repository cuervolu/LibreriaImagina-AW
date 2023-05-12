from django.shortcuts import render
from django.contrib.humanize.templatetags.humanize import intcomma
from .models import *


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
    return render(request, "auth/login.html")

