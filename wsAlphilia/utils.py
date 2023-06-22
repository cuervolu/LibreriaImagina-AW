import datetime
import logging
import random
from decouple import config
import requests

from libreria_imagina.models import Libro


def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    # Configurar el formateador del registro
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

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

    return logger


def obtener_portada_large(book_id):
    logger = setup_logger()
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
        large_thumbnail_url = (
            "https://islandpress.org/sites/default/files/default_book_cover_2015.jpg"
        )

    return large_thumbnail_url


def create_libro_from_data(data):
    logger = setup_logger()
    try:
        book_id = data.get("id")
        volume_info = data.get("volumeInfo", {})
        sale_info = data.get("saleInfo", {})

        isbn = volume_info.get("industryIdentifiers", [])[0].get(
            "identifier", "Sin ISBN"
        )
        existing_libro = Libro.objects.filter(isbn=isbn).first()

        if existing_libro:
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

        default_values = {
            "nombre_libro": volume_info.get("title", ""),
            "autor": volume_info.get("authors", ["Sin autor"])[0],
            "descripcion": volume_info.get("description", "Sin descripción"),
            "editorial": volume_info.get("publisher", "Sin editorial"),
            "precio_unitario": sale_info.get("retailPrice", {}).get(
                "amount", random.randint(8000, 45000)
            ),
            "portada": obtener_portada_large(book_id),
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
    except Exception as e:
        # Manejar errores relacionados con la creación del libro
        logger.error(
            f"Ocurrió un error al crear un libro desde los datos de la API: {e}"
        )
        return None
