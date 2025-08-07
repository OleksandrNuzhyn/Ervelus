from adrf import serializers
from .models import Style, Genre


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ['name']


class StyleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    is_available = serializers.BooleanField(read_only=True)

    class Meta:
        model = Style
        fields = ['id', 'name', 'genre', 'is_available'] 