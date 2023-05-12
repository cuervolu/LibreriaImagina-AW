from django.contrib import admin
from .models import *

# Register your models here.

class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('rut', 'nombre', 'apellido', 'username', 'correo', 'telefono', 'tipo_usuario')
    search_fields = ['rut', 'nombre', 'apellido', 'username', 'correo', 'telefono']
    list_filter = ['tipo_usuario']
class ComunaAdmin(admin.ModelAdmin):
    list_display = ('id_comuna', 'nombre_comuna', 'region')
    search_fields = ['nombre_comuna','region']
    list_filter = ['region']
class RegionAdmin(admin.ModelAdmin):
    list_display = ('id_region', 'nombre', 'numero_romano',)
    search_fields = ['id_region', 'nombre', 'numero_romano']
    list_filter = ['id_region']
class LibroAdmin(admin.ModelAdmin):
    list_display = ('id_libro', 'nombre_libro', 'autor','editorial', 'precio_unitario', 'categoria')
    search_fields = ['id_libro', 'nombre_libro', 'autor','editorial', 'precio_unitario']
    list_filter = ['categoria']
    

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(DetallePedido)
admin.site.register(Region, RegionAdmin)
admin.site.register(Comuna, ComunaAdmin)
admin.site.register(Direccion)
admin.site.register(Envio)
admin.site.register(Libro,LibroAdmin)

