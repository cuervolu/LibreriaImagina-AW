from rest_framework import serializers
from django.contrib.auth import authenticate

from .models import Libro, Usuario

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Autenticar al usuario utilizando el correo electrónico o el nombre de usuario
        user = None
        if username:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

        if not user:
            # Usuario no válido
            raise serializers.ValidationError('Credenciales inválidas')

        # Agregar el objeto user al contexto
        attrs['user'] = user
        return attrs