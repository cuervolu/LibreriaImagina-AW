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
    path("carrito", carrito, name="carrito"),
    path("catalogue", catalogue, name="catalogue"),
    path("books/<slug:slug>/", book_detail, name="book_detail"),
    # Incluir las URLs de autenticación desde auth.urls
    path("auth/", include(auth_urls, namespace="auth")),
    # Páginas Legales
    path("legal/terms_and_conditions",terms_and_conditions, name="terms_and_conditions"),
    path("legal/privacy",privacy, name="privacy")
]
