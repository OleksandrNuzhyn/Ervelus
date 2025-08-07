from adrf.serializers import ModelSerializer
from rest_framework import serializers
from .models import Style, Genre


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class StyleSerializer(ModelSerializer):
    genre = GenreSerializer()
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Style
        fields = ['id', 'name', 'genre', 'is_available'] 