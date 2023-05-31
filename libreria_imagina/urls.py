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
    path("purchase_detail", purchase_detail, name="purchase_detail"),
    path("shipments", shipments, name="shipments"),
    path("catalogue", catalogue, name="catalogue"),
    path("books/<slug:slug>/", book_detail, name="book_detail"),
    path("search", search, name="search"),
    path("profile", profile, name="profile"),
    path("my_data", my_data, name="my_data"),
    # Incluir las URLs de autenticación desde auth.urls
    path("auth/", include(auth_urls, namespace="auth")),
    # Páginas Legales
    path("legal/terms_and_conditions",terms_and_conditions, name="terms_and_conditions"),
    path("legal/privacy",privacy, name="privacy"),
    path('cart/eliminar/<int:detalle_carrito_id>/', eliminar_producto_carrito, name='eliminar_producto_carrito'),
    path('aumentar_cantidad/<int:detalle_carrito_id>/', aumentar_cantidad, name='aumentar_cantidad'),
    path('disminuir_cantidad/<int:detalle_carrito_id>/', disminuir_cantidad, name='disminuir_cantidad'),
]
