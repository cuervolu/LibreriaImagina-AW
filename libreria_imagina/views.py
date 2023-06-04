from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.humanize.templatetags.humanize import intcomma
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.urls import reverse
from django.utils.html import escapejs
from django.db.models import Sum, Q
from decimal import Decimal
from django.http import JsonResponse
from datetime import datetime

# importar una librería decoradora , permite evitar el ingreso de usuarios a la página web
from django.contrib.auth.decorators import login_required, permission_required

from django.core.paginator import Paginator

from libreria_imagina.utils import format_book_prices

from .models import *
from .forms import SignupForm

# **********************
# *       APP          *
# **********************


# Create your views here.
def index(request):
    # Se obtienen 10 libros aleatorios de la base de datos
    libros = list(Libro.objects.order_by("nombre_libro", "fecha_publicacion")[:10])
    libros = format_book_prices(libros)
    # Se crea un diccionario con los libros obtenidos para pasarlo al contexto
    context = {"libros": libros}
    # Se renderiza la plantilla 'index.html' con el contexto creado
    return render(request, "app/index.html", context)


def catalogue(request):
    libros = Libro.objects.all().order_by('nombre_libro')

    categorias = Libro.objects.values_list("categoria", flat=True).distinct()

    categoria_filtrada = request.GET.get("categoria")
    if categoria_filtrada:
        libros = libros.filter(categoria=categoria_filtrada)

    libros = format_book_prices(libros)  # Formatear los precios de los libros

    # Crear un objeto Paginator con la lista de libros y el número de libros por página
    paginator = Paginator(libros, 12)

    # Obtener el número de página solicitado de la consulta GET
    pagina_num = request.GET.get("pagina")

    # Obtener la página correspondiente al número de página solicitado
    pagina_libros = paginator.get_page(pagina_num)

    return render(
        request,
        "app/catalogue.html",
        {"libros": pagina_libros, "categorias": categorias, "categoria_filtrada": categoria_filtrada},
    )



# Detalle libro


def book_detail(request, slug):
    libro = get_object_or_404(Libro, slug=slug)

    # Actualizar http a https
    libros = Libro.objects.filter(portada__startswith="http://")

    for libro in libros:
        portada_url = libro.portada
        updated_url = portada_url.replace("http://", "https://")
        libro.portada = updated_url
        libro.save()

    libro = format_book_prices(libro)
    

    return render(request, "app/book_detail.html", {"libro": libro})


#Buscar Libro
def search(request):
    if request.method == "POST":
        searched = request.POST['search']
        # Buscar por título o autor
        entity = Libro.objects.filter(Q(nombre_libro__icontains=searched) | Q(autor__icontains=searched))
        
        entity = format_book_prices(entity)
        count = entity.count()
            
        # Crear un objeto Paginator con la lista de libros y el número de libros por página
        paginator = Paginator(entity, 12)

        # Obtener el número de página solicitado de la consulta GET
        pagina_num = request.GET.get("pagina")

        # Obtener la página correspondiente al número de página solicitado
        pagina_libros = paginator.get_page(pagina_num)
        return render(request, "app/search.html", {"searched": searched, "entity": pagina_libros, "count": count})
    else:
        return render(request, "app/search.html")




# **********************
# *       CARRITO      *
# **********************


@login_required(login_url="auth/login")
def agregar_al_carrito(request, id_libro):
    libro = get_object_or_404(Libro, id_libro=id_libro)

    # Obtener el carrito del usuario actual
    carrito, created = Carrito.objects.get_or_create(usuario=request.user)

    # Obtener la cantidad del formulario POST
    cantidad = int(request.POST.get("cantidad", 1))

    # Calcular el precio total
    precio_total = libro.precio_unitario * cantidad

    # Verificar si el libro ya está en el carrito
    detalle_carrito, created = DetalleCarrito.objects.get_or_create(
        carrito=carrito,
        libro=libro,
        defaults={"cantidad": cantidad, "precio_total": precio_total},
    )

    # Si el libro ya está en el carrito, incrementar la cantidad y actualizar el precio total
    if not created:
        detalle_carrito.cantidad += cantidad
        detalle_carrito.precio_total = libro.precio_unitario * detalle_carrito.cantidad
        detalle_carrito.save()

    # Incrementar la cantidad de libros en el carrito y reducir la cantidad disponible del libro
    carrito.cantidad += cantidad
    libro.cantidad_disponible -= cantidad
    libro.save()

    # Actualizar el total a pagar en el carrito
    carrito.total_pagar = DetalleCarrito.objects.filter(carrito=carrito).aggregate(
        total=Sum("precio_total")
    )["total"] or Decimal(0)
    carrito.save()

    return redirect("cart")  # Redirigir a la página del carrito


@login_required(login_url="auth/login")
def cart(request):
    envio = 3200
    try:
        carrito = Carrito.objects.get(usuario=request.user)
    except Carrito.DoesNotExist:
        carrito = Carrito.objects.create(usuario=request.user)

    detalle_carrito = carrito.detallecarrito_set.all()

    libros_filtrados = Libro.objects.filter(detallecarrito__carrito=carrito)

    libros_filtrados = format_book_prices(libros_filtrados)

    for detalle in detalle_carrito:
        detalle.precio_total = format(detalle.precio_total, ",.0f")

    total = carrito.total_pagar + envio

    carrito.total_pagar = format(carrito.total_pagar, ",.0f")

    context = {
        "carrito": carrito,
        "detalle_carrito": detalle_carrito,
        "libros_filtrados": libros_filtrados,
        "total": format(total, ",.0f"),
        "envio": format(envio, ",.0f"),
    }

    return render(request, "app/cart.html", context)

@login_required(login_url="auth/login")
def my_purchases(request):
    return render(request, "app/my_purchases.html")

@login_required(login_url="auth/login")
def purchase_detail(request):
    return render(request, "app/purchase_detail.html")

@login_required(login_url="auth/login")
def shipments(request):
    return render(request, "app/shipments.html")

@login_required(login_url="auth/login")
def profile(request):
    usuario = request.user
    
    datos = {
        'usuario' : usuario
    }
    return render(request, "app/profile.html", datos)

@login_required(login_url="auth/login")
def my_data(request):
    usuario = request.user
    regiones = Region.objects.all()
    selected_region_id = request.GET.get('region_id')  # Obtener el ID de la región seleccionada en el formulario
    direcciones = None

    if usuario.direccion:
        direcciones = Direccion.objects.filter(id_direccion=usuario.direccion.id_direccion)

    if selected_region_id:
        comunas = Comuna.objects.filter(region_id=selected_region_id)
    else:
        comunas = Comuna.objects.all()
    
    tarjetas = MetodoPago.objects.filter(usuario=usuario)
    
    datos = {
        'usuario' : usuario,
        'regiones' : regiones,
        'comunas' : comunas,
        'direcciones' : direcciones,
        'tarjetas' : tarjetas,
    }
    return render(request, "app/my_data.html", datos)


def obtener_comunas(request):
    selected_region_id = request.GET.get('region_id')
    if selected_region_id:
        comunas = Comuna.objects.filter(region_id=selected_region_id).values('nombre_comuna', 'id_comuna')
        return JsonResponse({'comunas': list(comunas)})
    else:
        return JsonResponse({'comunas': []})


@login_required(login_url="auth/login")
def cards(request):
    usuario = request.user
    tarjetas = MetodoPago.objects.filter(usuario=usuario)
    datos = {
        'usuario' : usuario,
        'tarjetas' : tarjetas,
    }
    return render(request, "app/cards.html", datos)

@login_required(login_url="auth/login")
def addresses(request):
    usuario = request.user
    regiones = Region.objects.all()
    selected_region_id = request.GET.get('region_id')  # Obtener el ID de la región seleccionada en el formulario
    direcciones = None

    if usuario.direccion:
        direcciones = Direccion.objects.filter(id_direccion=usuario.direccion.id_direccion)
    
    if selected_region_id:
        comunas = Comuna.objects.filter(region_id=selected_region_id)
    else:
        comunas = Comuna.objects.all()

    datos = {
        'usuario' : usuario,
        'regiones' : regiones,
        'comunas' : comunas,
        'direcciones' : direcciones
    }
    return render(request, "app/addresses.html", datos)

@login_required(login_url="auth/login")
def agregar_metodo_pago(request):
    usuario = request.user
    url_anterior = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        nombre_tarjeta = request.POST['nombre_tarjeta']
        nombre_titular = request.POST['nombre_titular']
        numero_tarjeta = request.POST['numero_tarjeta']
        fecha_vencimiento = request.POST['fecha_vencimiento']

        fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%m/%y').strftime('%Y-%m-%d')

        metodo_pago = MetodoPago()

        metodo_pago.usuario = usuario
        metodo_pago.metodo_nombre = nombre_tarjeta
        metodo_pago.tarjeta_numero = numero_tarjeta
        metodo_pago.tarjeta_nombre_titular = nombre_titular
        metodo_pago.fecha_vencimiento = fecha_vencimiento

        metodo_pago.save()
            
        # Redirigir al usuario después de procesar exitosamente el formulario POST
        return redirect(url_anterior)
    
@login_required(login_url="auth/login")
def eliminar_metodo_pago(request, metodo_pago_id):
    url_anterior = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        metodo_pago = MetodoPago.objects.get(id = metodo_pago_id)
        metodo_pago.delete()
            
        # Redirigir al usuario después de procesar exitosamente el formulario POST
        return redirect(url_anterior)

@login_required(login_url="auth/login")
def agregar_domicilio(request):
    usuario = request.user
    url_anterior = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        direccion = Direccion()
        direccion.direccion = request.POST['direccion']
        idcomuna = request.POST['idcomuna']
        comuna = Comuna.objects.get(id_comuna=idcomuna)
        direccion.comuna = comuna

        if usuario.direccion:
            usuario.direccion.delete()
            usuario.direccion = direccion
            usuario.save()
        else:
            usuario.direccion = direccion
            usuario.save()
            
        # Redirigir al usuario después de procesar exitosamente el formulario POST
        return redirect(url_anterior)

@login_required(login_url="auth/login")
def eliminar_domicilio(request, id_direccion):
    url_anterior = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        direccion = Direccion.objects.get(id_direccion = id_direccion)
        direccion.delete()
            
        # Redirigir al usuario después de procesar exitosamente el formulario POST
        return redirect(url_anterior)


@login_required(login_url="auth/login")
def eliminar_producto_carrito(request, detalle_carrito_id):
    try:
        detalle_carrito = DetalleCarrito.objects.get(id=detalle_carrito_id)
        carrito = Carrito.objects.get(id_carrito=detalle_carrito.carrito_id)
        libro = Libro.objects.get(id_libro=detalle_carrito.libro_id)

        # Actualizar la cantidad en el carrito y el libro
        carrito.cantidad -= detalle_carrito.cantidad
        libro.cantidad_disponible += detalle_carrito.cantidad

        # Actualizar el total_pagar en el carrito
        carrito.total_pagar -= detalle_carrito.precio_total

        detalle_carrito.delete()
        carrito.save()
        libro.save()
    except DetalleCarrito.DoesNotExist:
        pass

    return redirect("cart")


@login_required(login_url="auth/login")
def aumentar_cantidad(request, detalle_carrito_id):
    try:
        detalle_carrito = DetalleCarrito.objects.get(id=detalle_carrito_id)
        libro = Libro.objects.get(id_libro=detalle_carrito.libro_id)

        if detalle_carrito.cantidad < libro.cantidad_disponible:
            detalle_carrito.cantidad += 1
            libro.cantidad_disponible -= 1
            detalle_carrito.precio_total = (
                detalle_carrito.cantidad * libro.precio_unitario
            )
            detalle_carrito.save()
            libro.save()

            # Actualizar el total_pagar en el carrito
            carrito = Carrito.objects.get(id_carrito=detalle_carrito.carrito_id)
            carrito.total_pagar += libro.precio_unitario
            carrito.cantidad += 1
            carrito.save()

    except DetalleCarrito.DoesNotExist:
        pass

    return redirect("cart")


@login_required(login_url="auth/login")
def disminuir_cantidad(request, detalle_carrito_id):
    try:
        detalle_carrito = DetalleCarrito.objects.get(id=detalle_carrito_id)
        libro = Libro.objects.get(id_libro=detalle_carrito.libro_id)

        if detalle_carrito.cantidad > 1:
            detalle_carrito.cantidad -= 1
            libro.cantidad_disponible += 1
            detalle_carrito.precio_total = (
                detalle_carrito.cantidad * libro.precio_unitario
            )
            detalle_carrito.save()
            libro.save()

            # Actualizar el total_pagar en el carrito
            carrito = Carrito.objects.get(id_carrito=detalle_carrito.carrito_id)
            carrito.total_pagar -= libro.precio_unitario
            carrito.cantidad -= 1
            carrito.save()

    except DetalleCarrito.DoesNotExist:
        pass

    return redirect("cart")

@login_required(login_url="auth/login")
def imaginaPay(request):
    usuario = request.user
    tarjetas = MetodoPago.objects.filter(usuario=usuario)

    envio = 3200
    try:
        carrito = Carrito.objects.get(usuario=request.user)
    except Carrito.DoesNotExist:
        carrito = Carrito.objects.create(usuario=request.user)
    
    total = carrito.total_pagar + envio

    carrito.total_pagar = format(carrito.total_pagar, ",.0f")
    

    datos = {
        'usuario' : usuario,
        'tarjetas' : tarjetas,
        'carrito' : carrito,
        'total': format(total, ",.0f")
    }
    return render(request, "app/imaginaPay.html", datos)

@login_required(login_url="auth/login")
def generar_pago(request):
    url_anterior = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        metodo_pago_id = request.POST['flexRadioDefault']
        numero_tarjeta = request.POST['cardInput']
        metodo_pago = MetodoPago.objects.get(id = metodo_pago_id)
        
        if metodo_pago.tarjeta_numero == numero_tarjeta:
            print(metodo_pago.tarjeta_numero)
        else:
            print("No coincide")
            
        # Redirigir al usuario después de procesar exitosamente el formulario POST
        return redirect(url_anterior)


# **********************
# *       LEGAL        *
# **********************
def terms_and_conditions(request):
    return render(request, "app/legal/terms_and_conditions.html")


def privacy(request):
    return render(request, "app/legal/privacy.html")


# **********************
# *       AUTH       *
# **********************


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
            user = form.save()
            login(request, user)  # Autentica al usuario
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
