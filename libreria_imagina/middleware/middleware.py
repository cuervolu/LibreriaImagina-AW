import os
from pathlib import Path
from ..models import Carrito
from django.http import HttpResponse
from django.conf import settings
from django.template.loader import render_to_string

class CarritoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            usuario = request.user
            carrito = Carrito.objects.filter(usuario=usuario).first()
            if carrito:
                cantidad_elementos = carrito.cantidad
            else:
                cantidad_elementos = 0
            request.session["cantidad_carrito"] = cantidad_elementos

        response = self.get_response(request)

        return response

class DBLoaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Obtener la ubicación del archivo de plantilla relativa al directorio base del proyecto
        loader_template_path = os.path.join(settings.BASE_DIR, 'libreria_imagina/templates/preloader.html')
        self.loader_content = render_to_string(loader_template_path)

    def __call__(self, request):
        response = self.get_response(request)

        if 'loader_shown' not in request.COOKIES and self.loader_content:
            response.set_cookie('loader_shown', 'true', max_age=3600)  # Establecer una cookie que expire en 1 hora
            response.content = response.content.replace(b'<body>', b'<body>' + self.loader_content.encode())

        return response