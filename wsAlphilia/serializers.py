from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Libro, Usuario


class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'


class CreateLibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = ['nombre_libro', 'descripcion', 'autor', 'editorial', 'precio_unitario',
                  'cantidad_disponible', 'thumbnail', 'portada', 'fecha_publicacion', 'categoria', 'isbn']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['rut', 'nombre', 'apellido', 'username',
                  'correo', 'telefono', 'tipo_usuario', 'password']


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Autenticar al usuario utilizando el correo electrónico o el nombre de usuario
        user = None
        if username:
            user = authenticate(request=self.context.get(
                'request'), username=username, password=password)

        if not user:
            # Devolver un diccionario con los errores en lugar de lanzar la excepción
            errors = {'non_field_errors': ['Credenciales inválidas']}
            raise serializers.ValidationError(errors)

        # Agregar el objeto user al contexto
        attrs['user'] = user
        return attrs
