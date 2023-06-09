from django.urls import path, include
from .views import *
from .templates.auth import urls as auth_urls


urlpatterns = [
    path("", index, name="index"),
    path(
        "agregar_al_carrito/<int:id_libro>/",
        agregar_al_carrito,
        name="agregar_al_carrito",
    ),
    path("cart", cart, name="cart"),
    path("my_purchases", my_purchases, name="my_purchases"),
    path("purchase_detail/<int:pedido_id>", purchase_detail, name="purchase_detail"),
    path("shipments/<int:id_envio>", shipments, name="shipments"),
    path("catalogue", catalogue, name="catalogue"),
    path("books/<slug:slug>/", book_detail, name="book_detail"),
    path("search/", search, name="search"),
    path("profile", profile, name="profile"),
    path("support", support, name="support"),
    path("maintenance/<int:id_mantenimiento>", maintenance, name="maintenance"),
    path("my_data", my_data, name="my_data"),
    path("cambiar_username", cambiarUsername, name="cambiar_username"),
    path("cambiar_correo", cambiarCorreo, name="cambiar_correo"),
    path("change_password", changePassword, name="change_password"),
    path('obtener_comunas/', obtener_comunas, name='obtener_comunas'),
    path("obtener_libros/", obtener_libros, name="obtener_libros"),
    path("cards", cards, name="cards"),
    path("addresses", addresses, name="addresses"),
    path("imaginaPay", imaginaPay, name="imaginaPay"),
    path("generar_pago", generar_pago, name="generar_pago"),
    path("generar_mantenimiento", generar_mantenimiento, name="generar_mantenimiento"),
    # Incluir las URLs de autenticación desde auth.urls
    path("auth/", include(auth_urls, namespace="auth")),
    # Páginas Legales
    path("legal/terms_and_conditions",terms_and_conditions, name="terms_and_conditions"),
    path("legal/privacy",privacy, name="privacy"),
    path('cart/eliminar/<int:detalle_carrito_id>/', eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('aumentar_cantidad/<int:detalle_carrito_id>/', aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir_cantidad/<int:detalle_carrito_id>/', disminuir_cantidad, name='disminuir_cantidad'),
    path("agregar_domicilio", agregar_domicilio, name="agregar_domicilio"),
    path('eliminar_domicilio/<int:id_direccion>/', eliminar_domicilio, name='eliminar_domicilio'),
    path("agregar_metodo_pago", agregar_metodo_pago, name="agregar_metodo_pago"),
    path('eliminar_metodo_pago/<int:metodo_pago_id>/', eliminar_metodo_pago, name='eliminar_metodo_pago'),
    path('<str:exception>', error_404, name='404')

]

handler404 = error_404