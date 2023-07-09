import requests
import json

from rest_framework.response import Response
from rest_framework import viewsets, pagination, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate
from django.db.models import Q
from libreria_imagina.models import TipoUsuario

from .models import Libro
from .serializers import LibroSerializer, LoginSerializer, UserSerializer, CreateUserSerializer

from decouple import config
import traceback
from .utils import (
    create_libro,
    delete_libro,
    setup_logger,
    create_libro_from_data,
    update_libro,
)

# Create your views here.
logger = setup_logger()


class LibroPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.order_by("id_libro")
    serializer_class = LibroSerializer
    pagination_class = LibroPagination

    """
    Vista para obtener libros desde la API de Google Books y guardarlos en la base de datos.

    Parámetros de entrada:
        - request: La solicitud HTTP recibida.

    Parámetros de salida:
        - Response con los datos combinados de la API y la base de datos.

    Comportamiento:
        1. Obtiene la clave de la API de Google Books desde el archivo de entorno.
        2. Establece el número máximo de resultados por página.
        3. Obtiene el número de página de la solicitud y lo convierte en un entero.
        4. Calcula el índice de inicio para la página actual.
        5. Inicializa una lista para almacenar los libros creados.
        6. Inicializa un contador para el número de libros obtenidos.
        7. Realiza una solicitud a la API de Google Books para obtener los libros más relevantes.
        8. Verifica si se obtuvieron resultados de la API.
        9. Itera sobre los libros obtenidos y llama al método create_libro_from_data para crear objetos Libro.
        10. Añade los libros creados a la lista libros_creados.
        11. Actualiza el contador y el índice de inicio.
        12. Verifica si se han obtenido suficientes libros según el número máximo de resultados.
        13. Guarda los libros creados en la base de datos con el método create_libro_from_data.
        14. Obtiene todos los libros guardados de la base de datos.
         15. Pagina los resultados si es necesario.
        16. Serializar los libros obtenidos y los combina con los datos de la API.
        17. Retorna una Response con los datos combinados.

    Excepciones:
        - Si ocurre una excepción al hacer la solicitud a la API de Google Books, se registra el error y se relanza la excepción.
        - Si no se encuentran resultados en la API, se retorna una Response con el mensaje de error correspondiente.
        - Si ocurre una excepción al procesar los datos de la API, se registra el error y se retorna una Response con el mensaje de error correspondiente.

    """

    @action(detail=False, methods=["get"])
    def get_libros_from_api(self, request):
        # Obtener la clave de la API de Google Books desde el archivo de entorno
        api_key = config("GOOGLE_BOOKS_API_KEY")

        # Establecer el número máximo de resultados
        max_results = 40

        try:
            # Hacer una solicitud a la API de Google Books para obtener los libros más relevantes
            response = requests.get(
                f"https://www.googleapis.com/books/v1/volumes?q=*&key={api_key}&maxResults={max_results}&orderBy=relevance&projection=full"
            )
            response.raise_for_status()  # Lanza una excepción en caso de error HTTP
            data = response.json()
            if "items" not in data:
                return Response(
                    {"error": "No se encontraron resultados"},
                    status=status.HTTP_404_NOT_FOUND,
                )

            libros_creados = []
            for item in data.get("items", []):
                libro = create_libro_from_data(item)
                if libro:
                    libros_creados.append(libro)

            # Crear un objeto paginador y paginar los libros creados
            paginator = LibroPagination()
            paginated_libros = paginator.paginate_queryset(libros_creados, request)

            # Serializar los libros paginados
            serializer = LibroSerializer(paginated_libros, many=True)

            # Retornar la respuesta paginada
            return paginator.get_paginated_response(serializer.data)

        except requests.exceptions.RequestException as api_error:
            # Manejar errores relacionados con la API
            logger.error(
                f"Ocurrió un error al hacer la solicitud a la API: {api_error}"
            )
            logger.error(
                traceback.format_exc()
            )  # Registrar el traceback completo para obtener detalles específicos
            return Response(
                {
                    "error": f"Ocurrió un error al hacer la solicitud a la API: {api_error}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        except Exception as e:
            logger.error(
                f"Ocurrió un error general al procesar los datos de la API: {e}"
            )
            return Response(
                {
                    "error": f"Ocurrió un error general al procesar los datos de la API: {e}"
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

    @action(detail=False, methods=["get", "patch", "post"])
    def libros(self, request):
        if request.method == "GET":
            libros = Libro.objects.all()
            serializer = LibroSerializer(libros, many=True)
            return Response(serializer.data)
        if request.method == "POST":
            serializer = LibroSerializer(data=request.data)
            return create_libro(request, serializer)
        return Response(
            {"error": "Método HTTP no permitido."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    """
    Vista para obtener libros de una categoría específica desde la API de Google Books y guardarlos en la base de datos.

    Parámetros de entrada:
        - request: La solicitud HTTP recibida.
        - categoria: La categoría de libros a obtener.

    Parámetros de salida:
        - Response con los datos combinados de la API y la base de datos para la categoría especificada.

    Comportamiento:
        1. Verifica si se proporcionó una categoría.
        2. Filtra los libros en la base de datos por la categoría especificada.
        3. Verifica si existen libros en la categoría.
        4. Serializa los libros obtenidos de la base de datos.
        5. Inicializa una lista para almacenar los libros creados.
        6. Realiza una solicitud a la API de Google Books para obtener los libros de la categoría especificada.
        7. Verifica si se obtuvieron resultados de la API.
        8. Itera sobre los libros obtenidos de la API y llama al método create_libro_from_data para crear objetos Libro.
        9. Añade los libros creados a la lista libros_creados.
        10. Serializa los libros creados.
        11. Combina los datos de la API y los datos de la base de datos.
        12. Retorna una Response con los datos combinados.

    Excepciones:
        - Si ocurre una excepción al hacer la solicitud a la API de Google Books, se registra el error y se retorna una Response con el mensaje de error correspondiente.
        - Si ocurre una excepción al procesar los datos de la API, se registra el error y se retorna una Response con el mensaje de error correspondiente.

    """

    @action(detail=False, methods=["get"])
    def get_libros_by_categoria(self, request, categoria=None):
        if categoria:
            # Obtener la clave de la API de Google Books desde el archivo de entorno
            api_key = config("GOOGLE_BOOKS_API_KEY")

            # Hacer una solicitud a la API de Google Books para obtener los libros de la categoría especificada
            try:
                response = requests.get(
                    f"https://www.googleapis.com/books/v1/volumes?q=subject:{categoria}&key={api_key}"
                )
                response.raise_for_status()
                data = response.json()
                response.close()
                libros_creados = []
                for item in data.get("items", []):
                    libro = create_libro_from_data(item)
                    if libro:
                        libros_creados.append(libro)
                print(libros_creados)
                libros_creados_serializados = LibroSerializer(
                    libros_creados, many=True
                ).data
                return Response(libros_creados_serializados)
            except (
                requests.exceptions.RequestException,
                json.JSONDecodeError,
            ) as e:
                logger.error(f"Error al obtener los libros de la API: {e}")
                logger.error(
                    traceback.format_exc()
                )  # Registrar el traceback completo para obtener detalles específicos
                return Response(
                    {"error": f"Error al obtener los libros de la API: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "La categoría no fue proporcionada."},
                status=status.HTTP_400_BAD_REQUEST,
            )

    """
    Vista para obtener o actualizar un libro específico.

    Parámetros de entrada:
        - request: La solicitud HTTP recibida.
        - pk: La clave primaria del libro a obtener o actualizar.

    Parámetros de salida:
        - Response con los datos del libro solicitado o actualizado.

    Comportamiento:
        1. Intenta obtener el libro de la base de datos utilizando la clave primaria proporcionada.
        2. Verifica si el libro existe en la base de datos.
        3. Si la solicitud HTTP es GET, serializa el libro y retorna una Response con los datos del libro.
        4. Si la solicitud HTTP es PUT, actualiza el libro con los datos proporcionados en la solicitud.
        5. Verifica si los datos para la actualización son válidos.
        6. Si los datos son válidos, guarda los cambios y retorna una Response con los datos actualizados del libro.
        7. Si los datos no son válidos, retorna una Response con los errores de validación.

    Excepciones:
        - Si el libro no existe en la base de datos, retorna una Response con el mensaje de error correspondiente.

    """

    @action(detail=True, methods=["get", "patch", "delete"])
    def libro_detail(self, request, pk=None):
        try:
            libro = Libro.objects.get(id_libro=pk)
        except Libro.DoesNotExist:
            return Response(
                {"error": "El libro no existe."}, status=status.HTTP_404_NOT_FOUND
            )

        if request.method == "GET":
            serializer = LibroSerializer(libro)
            return Response(serializer.data)
        elif request.method == "PATCH":
            return update_libro(request, libro)
        elif request.method == "DELETE":
            delete_libro(libro)
            return Response(status=status.HTTP_204_NO_CONTENT)


# **********************
# *       AUTH       *
# **********************


class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data.get("username")
            email = serializer.validated_data.get("email")
            password = serializer.validated_data["password"]

            # Autenticar al usuario utilizando el correo electrónico o el nombre de usuario
            user = None
            if email:
                user = authenticate(request, email=email, password=password)
            elif username:
                user = authenticate(request, username=username, password=password)

            if user:
                # Validar el rol del usuario
                if user.tipo_usuario not in [
                    TipoUsuario.ADMIN,
                    TipoUsuario.TECNICO,
                    TipoUsuario.ENCARGADO_BODEGA,
                    TipoUsuario.EMPLEADO,
                    TipoUsuario.REPARTIDOR,
                ]:
                    # Usuario no válido debido a falta de permisos
                    logger.warning(
                        "Intento de inicio de sesión fallido debido a falta de permisos"
                    )
                    return Response(
                        {"error": "Falta de permisos"}, status=status.HTTP_403_FORBIDDEN
                    )

                # Generar o recuperar el token de autenticación
                token, created = Token.objects.get_or_create(user=user)

                # Registrar evento de inicio de sesión exitoso
                logger.info(
                    f"Inicio de sesión exitoso para el usuario: {user.username}"
                )

                # Devolver la respuesta con el token y los datos del usuario
                user_serializer = UserSerializer(user)
                return Response({"token": token.key, "user": user.pk})
            else:
                # Usuario no válido
                logger.warning("Intento de inicio de sesión fallido")
                return Response(
                    {"non_field_errors": ["Credenciales inválidas"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except ValidationError as e:
            # Capturar la excepción ValidationError
            errors = e.get_full_details()

            # Devolver una respuesta con los errores personalizados
            return Response(errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Registrar el error en el log
            logger.exception("Error en el inicio de sesión: %s", str(e))
            # Devolver una respuesta de error adecuada
            return Response(
                {"error": "Error en el inicio de sesión"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        # Invalidar el token de autenticación del usuario
        if request.auth:
            request.auth.delete()
            logger.info(f"Cierre de sesión exitoso para el usuario")

        return Response({"detail": "Cierre de sesión exitoso."})


class CreateUserView(APIView):
    def post(self, request, format=None):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            tipo_usuario = request.data.get('tipo_usuario')
            
            if tipo_usuario in TipoUsuario.values:
                # Obtén la contraseña en texto plano del serializer
                password = serializer.validated_data['password']

                # Crea una instancia de Usuario sin guardarla aún
                usuario = serializer.save(tipo_usuario=tipo_usuario)

                # Establece la contraseña en su forma encriptada
                usuario.set_password(password)
                
                # Establece el atributo is_staff si corresponde
                if tipo_usuario != TipoUsuario.CLIENTE:
                    usuario.is_staff = True

                # Guarda el usuario en la base de datos
                usuario.save()

                return Response({'message': 'Usuario creado exitosamente', 'id': usuario.id}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Tipo de usuario inválido'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            error_message = "Error al crear el usuario."
            if serializer.errors:
                error_message += f" Detalles: {serializer.errors}"
            return Response({'message': error_message}, status=status.HTTP_400_BAD_REQUEST)