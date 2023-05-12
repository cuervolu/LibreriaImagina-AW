from django.urls import path, include
from .views import *
from .templates.auth import urls as auth_urls


urlpatterns = [
    path('', index, name = 'index'),

    # Incluir las URLs de autenticación desde auth.urls
    path('auth/', include(auth_urls, namespace='auth'))
]

