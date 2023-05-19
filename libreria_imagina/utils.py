from libreria_imagina.models import Libro


def format_book_prices(libros):
    if isinstance(libros, Libro):  # Verificar si es un solo objeto Libro
        libros.precio_unitario = format(libros.precio_unitario, ",.0f")
    else:  # Es una lista de libros
        for libro in libros:
            libro.precio_unitario = format(libro.precio_unitario, ",.0f")
    return libros
