from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Libro

class LibroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Libro
        fields = '__all__'



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=False)
    password = serializers.CharField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # Si se proporciona un correo electrónico válido, asumir que se ingresó un correo electrónico
        if username and '@' in username:
            attrs['email'] = username
            del attrs['username']
        return attrs
