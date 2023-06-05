import cx_Oracle
from django.conf import settings

def get_connection():
    return cx_Oracle.connect(
        settings.DATABASES['default']['USER'],
        settings.DATABASES['default']['PASSWORD'],
        f"{settings.DATABASES['default']['HOST']}:{settings.DATABASES['default']['PORT']}/{settings.DATABASES['default']['NAME']}"
    )

def get_categories():
    conn = get_connection()
    cursor = conn.cursor()
    
    resultado = cursor.var(cx_Oracle.CURSOR)
    
    cursor.callproc('listar_categorias', [resultado])
    
     # Recupera los resultados del cursor
    categorias = resultado.getvalue().fetchall()

    cursor.close()
    conn.close()

    return categorias
    
def get_numbers_of_books():
    conn = get_connection()
    cursor = conn.cursor()
    
    cantidad = cursor.var(cx_Oracle.NUMBER)
    
    cursor.callproc('MostrarCantidadLibros', [cantidad])
    
    cantidad_libros = int(cantidad.getvalue())
    
    cursor.close()
    conn.close()

    return cantidad_libros