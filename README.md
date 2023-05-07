
# Aplicación Web de Librería Imagina

Libreria Imagina es un proyecto web basado en Django, que utiliza un archivo de configuración `.env` y una base de datos Oracle. Este proyecto tiene como objetivo proporcionar una plataforma para la gestión de una librería virtual, permitiendo a los usuarios realizar búsquedas y compras de libros.

## Configuración

Para ejecutar este proyecto, debes seguir los siguientes pasos:

1. Clona este repositorio en tu máquina local.
2. Crea un entorno virtual de Python en la carpeta raíz del proyecto.
3. Activa el entorno virtual con `<nombreEntorno>\Scripts\activate`
4. Instala Django con `pip install django`
5. Asegúrate de tener una base de datos Oracle instalada y configurada en tu máquina local.
6. Ejecuta `python manage.py migrate` para aplicar las migraciones y crear las tablas de la base de datos.
7. Ejecuta `python manage.py runserver` para iniciar el servidor de desarrollo de Django.

#

Si deseas verificar en la consola si la conexión a la base de datos a sido exitosa, debes ejecutar el siguiente comando:

``python manage.py dbshell``

El comando python manage.py dbshell se utiliza para acceder a la consola de la base de datos. Una vez dentro de la consola de la base de datos, puedes ejecutar diferentes comandos dependiendo del tipo de base de datos que estés utilizando. A continuación, se muestran algunos de los comandos comunes que se pueden utilizar en la consola de la base de datos:

- SELECT: Se utiliza para seleccionar datos de una o más tablas de la base de datos.
- INSERT: Se utiliza para insertar nuevos datos en una tabla de la base de datos.
- UPDATE: Se utiliza para actualizar datos existentes en una tabla de la base de datos.
- DELETE: Se utiliza para eliminar datos de una tabla de la base de datos.
- CREATE: Se utiliza para crear una nueva tabla, vista, índice u otro objeto de base de datos.
- ALTER: Se utiliza para modificar la estructura de una tabla existente.
- DROP: Se utiliza para eliminar una tabla, vista, índice u otro objeto de la base de datos.
- SHOW: Se utiliza para mostrar información sobre la estructura o configuración de la base de datos.
- DESCRIBE: Se utiliza para mostrar la estructura de una tabla o vista.
- TRUNCATE: Se utiliza para eliminar todos los registros de una tabla sin eliminar la estructura de la tabla.

## Estructura de Archivos

El proyecto sigue la estructura de archivos típica de un proyecto Django, con algunos archivos adicionales para el soporte de Typescript y la configuración de variables de entorno:

```
libreriaimagina/
┣ core/                   # Configuraciones generales del proyecto
┃ ┣ asgi.py               # Archivo de punto de entrada para ASGI (Asynchronous Server Gateway Interface)
┃ ┣ settings.py           # Configuraciones principales del proyecto (base de datos, aplicaciones instaladas, etc.)
┃ ┣ urls.py               # Archivo de definición de URLs del proyecto
┃ ┣ wsgi.py               # Archivo de punto de entrada para WSGI (Web Server Gateway Interface)
┃ ┗ __init__.py           # Archivo que indica que la carpeta es un paquete de Python
┣ libreria_imagina/       # Aplicación específica de la librería
┃ ┣ static/               # Archivos estáticos (CSS, JS, imágenes, etc.)
┃ ┣ templates/            # Plantillas HTML de la aplicación
┃ ┣ admin.py              # Archivo de configuración del panel de administración de Django
┃ ┣ apps.py               # Archivo de configuración de la aplicación
┃ ┣ models.py             # Archivo de definición de los modelos de la aplicación
┃ ┣ tests.py              # Archivo de pruebas de la aplicación
┃ ┣ urls.py               # Archivo de definición de URLs de la aplicación
┃ ┣ views.py              # Archivo de definición de las vistas de la aplicación
┃ ┗ __init__.py           # Archivo que indica que la carpeta es un paquete de Python
┣ .env                    # Archivo que contiene las variables de entorno del proyecto
┣ .gitignore              # Archivo de configuración de Git para ignorar archivos y carpetas en el repositorio
┣ manage.py               # Archivo de gestión de Django
┣ README.md               # Archivo de documentación del proyecto
┗ requirements.txt        # Archivo que lista las dependencias del proyecto

```

## Variables de Entorno

Para ejecutar este proyecto, deberá agregar las siguientes variables de entorno a su archivo .env

`DEBUG`

`DB_NAME`

`DB_USER`

`DB_PASSWORD`

`DB_HOST`

`DB_PORT`

`ALLOWED_HOSTS`

El archivo `settings.py` ya viene configurado para utilizarlas.
