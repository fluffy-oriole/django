from rest_framework import serializers
from films.models import Actor, Director, Film, Genre, Review


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = "__all__"


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"


class FilmSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(read_only=True)
    directors = DirectorSerializer(read_only=True)
    actors = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Film
        fields = ['id', 'name', 'genre', 'release_date', 'rating', 'directors', 'actors']


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"