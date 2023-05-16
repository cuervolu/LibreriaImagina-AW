from django.urls import path, include
from .views import *
from .templates.auth import urls as auth_urls


urlpatterns = [
    path('', index, name = 'index'),
    path('agregar_al_carrito/<int:id_libro>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito', carrito, name = 'carrito'),

    # Incluir las URLs de autenticación desde auth.urls
    path('auth/', include(auth_urls, namespace='auth'))
]

