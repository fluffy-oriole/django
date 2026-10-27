from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from films.models import Collection, Director, Film, Genre, Review, Actor
from films.serializers import DirectorSerializer, FilmSerializer, GenreSerializer, ReviewSerializer, ActorSerializer, CollectionSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from rest_framework.decorators import action


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

class CollectionsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class ProfileViewSet(GenericViewSet):
    queryset = User.objects.all()

    @action(detail=False, url_path='me', methods=['GET'])
    def get_me(self, request, *args, **kwargs):
        data = {
            'is_authenticated': self.request.user.is_authenticated
        }
        if self.request.user.is_authenticated:
            data.update({
                "user_name": self.request.user.username,
                "id": self.request.user.id,
                "role": self.request.user.profile.role
            })
        return Response(data=data)

    @action(detail=False, url_path='logout', methods=['POST'])
    def logout(self, *args, **kwargs):
        django_logout(self.request)

        return Response()


    @action(detail=False, url_path='login', methods=['POST'])
    def login(self, *args, **kwargs):
        username = self.request.data['username']
        password = self.request.data['password']

        success = False
        status_code = 403

        user = authenticate(username=username, password=password)
        if user:
            success = True
            status_code = 200
            django_login(self.request, user)

        return Response({'success': success, 'status': status_code})