from django.urls import path
from .views import LibroViewSet, LoginView, LogoutView

urlpatterns = [
    path(
        "libros/",
        LibroViewSet.as_view({"get": "list", "post": "create"}),
        name="libro-list",
    ),
    path(
        "libros/<int:pk>/",
        LibroViewSet.as_view(
            {
                "get": "retrieve",
                "put": "update",
                "patch": "partial_update",
                "delete": "destroy",
            }
        ),
        name="libro-detail",
    ),
    path(
        "libros/get_libros_from_api/",
        LibroViewSet.as_view({"get": "get_libros_from_api"}),
        name="libro-get-libros-from-api",
    ),
    path(
        "libros/get_libros_by_categoria/<str:categoria>/",
        LibroViewSet.as_view({"get": "get_libros_by_categoria"}),
        name="libro-get-libros-by-categoria",
    ),
    # Otras rutas
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

