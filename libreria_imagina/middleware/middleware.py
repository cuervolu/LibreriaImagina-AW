from ..models import Carrito

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
            request.cantidad_carrito = cantidad_elementos

        response = self.get_response(request)

        return response
