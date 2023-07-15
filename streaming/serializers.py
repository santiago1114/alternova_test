from .models import Genre, Type, Stream
from rest_framework import serializers


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'
        
class StreamSerializer(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='type'
    )
    genre = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='genre'
    )
    class Meta:
        model = Stream
        fields = '__all__'