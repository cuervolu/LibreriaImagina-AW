from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils.html import escapejs

from .models import *
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

def agregar_al_carrito(request, id_libro, cantidad=1):
    libro = get_object_or_404(Libro, id_libro=id_libro)

    # Obtener el carrito del usuario actual
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)
    
     # Incrementar la cantidad de libros en el carrito
    carrito.cantidad += cantidad
    
     # Actualizar el total a pagar en el carrito
    carrito.total_pagar += libro.precio_unitario
    
    carrito.total_pagar += libro.precio_unitario

    # Guardar los cambios en el carrito
    carrito.save()


    return redirect('carrito')  # Redirigir a la página del carrito

def carrito(request):
    carrito = Carrito.objects.get(usuario=request.user)
    
    return render(request, "app/carrito.html", {"carrito": carrito})


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


def logout_view(request):
    logout(request)
    return redirect(
        "index"
    )  # Redireccionar a la página principal si se accede a la vista por GET
