from django.shortcuts import render

# Create your views here.
import datetime
import logging


import random
import requests
import json

from rest_framework.response import Response
from rest_framework import viewsets, pagination, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from django.contrib.auth import authenticate
from libreria_imagina.models import TipoUsuario, Usuario

from .models import Libro
from .serializers import LibroSerializer, LoginSerializer, UserSerializer

from decouple import config
import traceback

# Create your views here.
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Configurar el formateador del registro
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Configurar un controlador de archivo para registrar los mensajes de error
file_handler = logging.FileHandler("errors.log")
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# Configurar un controlador de registro para mostrar los mensajes en la consola
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Agregar los controladores al registro
logger.addHandler(file_handler)
logger.addHandler(console_handler)


class LibroPagination(pagination.PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 1000


class LibroViewSet(viewsets.ModelViewSet):
    queryset = Libro.objects.order_by("nombre_libro")
    serializer_class = LibroSerializer
    pagination_class = LibroPagination

    def obtener_portada_large(self, book_id):
        api_key = config("GOOGLE_BOOKS_API_KEY")

        # Construir la URL de la API de Google Books para obtener la información con la portada large del libro
        url = f"https://www.googleapis.com/books/v1/volumes/{book_id}?projection=full&key={api_key}"

        # Realizar la solicitud a la API de Google Books
        try:
            response = requests.get(url)
            data = response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Ocurrió un error al hacer la solicitud: {e}")
            raise

        # Obtener la URL de la portada "large"
        image_links = data.get("volumeInfo", {}).get("imageLinks", {})
        large_thumbnail_url = image_links.get("large")
        medium_thumbnail_url = image_links.get("medium")

        # Si no hay portada "large", intentar con la portada "medium"
        if not large_thumbnail_url:
            large_thumbnail_url = medium_thumbnail_url

        # Si aún no hay URL de la portada, utilizar la imagen predeterminada
        if not large_thumbnail_url:
            large_thumbnail_url = "https://islandpress.org/sites/default/files/default_book_cover_2015.jpg"

        return large_thumbnail_url

    def create_libro_from_data(self, data, _=None):
        book_id = data.get("id")
        volume_info = data.get("volumeInfo", {})
        sale_info = data.get("saleInfo", {})

        isbn = volume_info.get("industryIdentifiers", [])[0].get("identifier", "s/e")
        nombre_libro = volume_info.get("title", "")
        autor = volume_info.get("authors", ["a/d"])[0]

        if Libro.objects.filter(
            isbn=isbn, nombre_libro=nombre_libro, autor=autor
        ).exists():
            return None

        if "categories" in volume_info:
            categorias = volume_info.get("categories")
            if categorias:
                categoria = categorias[0]
            else:
                categoria = "General"
        else:
            categoria = "General"

        fecha_publicacion = volume_info.get("publishedDate")

        if not fecha_publicacion:
            current_year = datetime.datetime.now().year
            fecha_publicacion = datetime.datetime(
                current_year,
                random.randint(1, 12),
                random.randint(1, 28),
            ).strftime("%Y-%m-%d")

        try:
            datetime.datetime.strptime(fecha_publicacion, "%Y-%m-%d")
        except ValueError as e:
            year = random.randint(1960, 2023)
            month = random.randint(1, 12)
            day = random.randint(1, 28)
            fecha_publicacion = datetime.datetime(year, month, day).strftime("%Y-%m-%d")
            logger.error(f"Error al analizar la fecha de publicación: {e}")
            logger.error(
                traceback.format_exc()
            )  # Registrar el traceback completo para obtener detalles específicos

        default_values = {
            "nombre_libro": volume_info.get("title", ""),
            "autor": volume_info.get("authors", ["Sin autor"])[0],
            "descripcion": volume_info.get("description", "Sin descripción"),
            "editorial": volume_info.get("publisher", "Sin editorial"),
            "precio_unitario": sale_info.get("retailPrice", {}).get(
                "amount", random.randint(8000, 45000)
            ),
            "portada": self.obtener_portada_large(book_id),
            "thumbnail": volume_info.get("imageLinks", {}).get(
                "thumbnail",
                "https://islandpress.org/sites/default/files/default_book_cover_2015.jpg",
            ),
            "cantidad_disponible": random.randint(1, 150),
            "fecha_publicacion": fecha_publicacion,
            "categoria": categoria,
            "isbn": volume_info.get("industryIdentifiers", [])[0].get(
                "identifier", "Sin ISBN"
            ),
        }

        libro = Libro.objects.create(**default_values)
        return libro


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
        13. Guarda los libros creados en la base de datos utilizando el método bulk_create.
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

        # Establecer el número máximo de resultados por página
        max_results = 40

        # Obtener el número de página de la solicitud
        page_number = request.query_params.get("page", "1")
        page_number = int(page_number)  # convierte el valor en un entero

        # Calcular el índice de inicio para la página actual
        start_index = (page_number - 1) * max_results + 1

        libros_creados = []
        count = 0
        while count < max_results:
            # Hacer una solicitud a la API de Google Books para obtener los libros más relevantes
            try:
                response = requests.get(
                    f"https://www.googleapis.com/books/v1/volumes?q=*&key={api_key}&startIndex={start_index}&maxResults={max_results}&orderBy=relevance&random={random.random()}&projection=full"
                )
            except requests.exceptions.RequestException as e:
                logger.error(f"Ocurrió un error al hacer la solicitud: {e}")
                logger.error(
                    traceback.format_exc()
                )  # Registrar el traceback completo para obtener detalles específicos
                raise
            try:
                data = json.loads(response.content)
                response.close()
                if "items" not in data:
                    data = json.loads(response.content)
                response.close()
                if "items" not in data:
                    return Response(
                        {"error": "No se encontraron resultados"},
                        status=status.HTTP_404_NOT_FOUND,
                    )

                for item in data.get("items", []):
                    libro = self.create_libro_from_data(item)
                    if libro:
                        libros_creados.append(libro)

                    count += 1
                    start_index += 1

                    if count >= max_results:
                        break

                # Guardar los libros creados en la base de datos
                Libro.objects.bulk_create(libros_creados)

                # Obtener todos los libros guardados y serializarlos para enviarlos en la respuesta
                libros = Libro.objects.all()
                page = self.paginate_queryset(libros)
                if page is not None:
                    serializer = LibroSerializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                serializer = LibroSerializer(libros, many=True)
                combined_data = {"api_data": data, "db_data": serializer}
                return Response(combined_data)
            except Exception as e:
                logger.error(f"Ocurrió un error al procesar los datos de la API: {e}")
                return Response(
                    {"error": f"Ocurrió un error al procesar los datos de la API: {e}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
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
            libros = Libro.objects.filter(categoria=categoria)
            if libros.exists():
                serializer = LibroSerializer(libros, many=True)
                response_data = serializer.data
            else:
                response_data = []

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

            libros_creados = []
            for item in data.get("items", []):
                libro = self.create_libro_from_data(item)
                if libro:
                    libros_creados.append(libro)

            serializer = LibroSerializer(libros_creados, many=True)
            combined_data = {"api_data": data, "db_data": response_data}
            return Response(combined_data)
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


         
    @action(detail=True, methods=['get', 'put'])
    def libro_detail(self, request, pk=None):
        try:
            libro = Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            return Response({'error': 'El libro no existe.'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            serializer = LibroSerializer(libro)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = LibroSerializer(libro, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# **********************
# *       AUTH       *
# **********************

class LoginView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data.get('username')
            email = serializer.validated_data.get('email')
            password = serializer.validated_data['password']

            # Autenticar al usuario utilizando el correo electrónico o el nombre de usuario
            user = None
            if email:
                user = authenticate(request, email=email, password=password)
            elif username:
                user = authenticate(request, username=username, password=password)

            if user:
                # Validar el rol del usuario
                if user.tipo_usuario not in [TipoUsuario.ADMIN, TipoUsuario.TECNICO, TipoUsuario.ENCARGADO_BODEGA]:
                    # Usuario no válido debido a falta de permisos
                    logger.warning("Intento de inicio de sesión fallido debido a falta de permisos")
                    return Response({'error': 'Falta de permisos'}, status=status.HTTP_403_FORBIDDEN)
                

                # Generar o recuperar el token de autenticación
                token, created = Token.objects.get_or_create(user=user)

                # Registrar evento de inicio de sesión exitoso
                logger.info(f"Inicio de sesión exitoso para el usuario: {user.username}")
                
                # Devolver la respuesta con el token y los datos del usuario
                user_serializer = UserSerializer(user)
                return Response({'token': token.key, 'user': user_serializer.data})
            else:
                # Usuario no válido
                logger.warning("Intento de inicio de sesión fallido")
                return Response({'non_field_errors': ['Credenciales inválidas']}, status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            # Capturar la excepción ValidationError
            errors = e.get_full_details()

            # Devolver una respuesta con los errores personalizados
            return Response(errors, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            # Registrar el error en el log
            logger.exception("Error en el inicio de sesión: %s", str(e))
            # Devolver una respuesta de error adecuada
            return Response({'error': 'Error en el inicio de sesión'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)