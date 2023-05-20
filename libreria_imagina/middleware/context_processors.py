def cantidad_carrito(request):
    return {"cantidad_carrito": request.session.get('cantidad_carrito', 0)}
