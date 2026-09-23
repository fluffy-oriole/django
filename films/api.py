from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from films.models import Director, Film, Genre, Review, Actor
from films.serializers import DirectorSerializer, FilmSerializer, GenreSerializer, ReviewSerializer, ActorSerializer



class FilmsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

class GenresViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class ActorsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class DirectorsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer

class ReviewsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer