from .models import Genre, Type, Stream
from rest_framework import serializers
from django.contrib.auth.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
        
class StreamSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Stream
        fields = ['name', 'genre', 'type', 'views', 'score']
    
class StreamDetailViewSet(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='name', queryset=Genre.objects.all()
    )
    type = serializers.SlugRelatedField(
        slug_field='name', queryset=Genre.objects.all()
    )

    class Meta:
        model = Stream
        fields = ['name', 'genre', 'type', 'views', 'score']