from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework import serializers, mixins
from films.models import Collection, Director, Film, FilmImages, Genre, Review, Actor, Profile
from films.serializers import DirectorSerializer, FilmImagesSerializer, FilmSerializer, GenreSerializer, ReviewSerializer, ActorSerializer, CollectionSerializer, ProfileSerializer
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from django.contrib.auth import login as django_login
from django.contrib.auth import authenticate
from rest_framework.decorators import action
from django.db.models import Count, Avg, Min, Max
from django.db.models.functions import ExtractYear


class FilmsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user):
            if self.request.user.is_superuser:
                user_id = self.request.query_params.get('userId')
                if user_id:
                    return qs.filter(user_id=user_id)
                else:
                    return qs
            else:
                return qs.filter(user=self.request.user)


    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()
        

    @action(detail=False, url_path='stats', methods=['GET'])
    def get_stats(self, *args, **kwargs):
        stats = Film.objects.aggregate(
            count=Count('id'),
            avg=Avg('rating'),
            max=Max('rating'),
            min=Min('rating'),
        )

        serealizer = self.StatsSerializer(instance=stats)
        return Response(data=serealizer.data)

class GenresViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user):
            if self.request.user.is_superuser:
                user_id = self.request.query_params.get('userId')
                if user_id:
                    return qs.filter(user_id=user_id)
                else:
                    return qs
            else:
                return qs.filter(user=self.request.user)

    class StatsSerializer(serializers.Serializer):
            count = serializers.IntegerField()
            
    
    @action(detail=False, url_path='stats', methods=['GET'])
    def get_stats(self, *args, **kwargs):
        stats = Genre.objects.aggregate(
            count=Count('id'),
        )

        serealizer = self.StatsSerializer(instance=stats)
        return Response(data=serealizer.data)

class ActorsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user):
            if self.request.user.is_superuser:
                user_id = self.request.query_params.get('userId')
                if user_id:
                    return qs.filter(user_id=user_id)
                else:
                    return qs
            else:
                return qs.filter(user=self.request.user)


    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, url_path='stats', methods=['GET'])
    def get_stats(self, *args, **kwargs):
        stats = Actor.objects.aggregate(
            count=Count('id'),
            avg=Avg(ExtractYear('birth_date')),
            max=Max(ExtractYear('birth_date')),
            min=Min(ExtractYear('birth_date')),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(data=serializer.data)

class DirectorsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user):
            if self.request.user.is_superuser:
                user_id = self.request.query_params.get('userId')
                if user_id:
                    return qs.filter(user_id=user_id)
                else:
                    return qs
            else:
                return qs.filter(user=self.request.user)

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, url_path='stats', methods=['GET'])
    def get_stats(self, *args, **kwargs):
        stats = Director.objects.aggregate(
            count=Count('id'),
            avg=Avg(ExtractYear('birth_date')),
            max=Max(ExtractYear('birth_date')),
            min=Min(ExtractYear('birth_date')),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(data=serializer.data)

class ReviewsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user):
            if self.request.user.is_superuser:
                user_id = self.request.query_params.get('userId')
                if user_id:
                    return qs.filter(user_id=user_id)
                else:
                    return qs
            else:
                return qs.filter(user=self.request.user)

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.IntegerField()
        min = serializers.IntegerField()

    @action(detail=False, url_path='stats', methods=['GET'])
    def get_stats(self, *args, **kwargs):
        stats = Review.objects.aggregate(
            count=Count('id'),
            avg=Avg('rate'),
            max=Max('rate'),
            min=Min('rate'),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(data=serializer.data)

class CollectionsViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer


    def get_queryset(self):
        qs = super().get_queryset()
        if (self.request.user):
            if self.request.user.is_superuser:
                user_id = self.request.query_params.get('userId')
                if user_id:
                    return qs.filter(user_id=user_id)
                else:
                    return qs
            else:
                return qs.filter(user=self.request.user)

    class StatsSerializer(serializers.Serializer):
        count = serializers.IntegerField()
        avg = serializers.FloatField()
        max = serializers.FloatField()
        min = serializers.FloatField()

    @action(detail=False, url_path='stats', methods=['GET'])
    def get_stats(self, *args, **kwargs):
        stats = Collection.objects.aggregate(
            count=Count('id'),
            avg=Avg('price'),
            max=Max('price'),
            min=Min('price'),
        )

        serializer = self.StatsSerializer(instance=stats)
        return Response(data=serializer.data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UsersViewset(mixins.ListModelMixin,
                GenericViewSet):
    queryset = User.objects.all().filter(profile__role=Profile.Role.user).select_related('profile')
    serializer_class = UserSerializer

class ProfileViewSet(mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


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


class FilmsImagesViewset(
                mixins.ListModelMixin,
                mixins.CreateModelMixin,
                mixins.UpdateModelMixin,
                mixins.RetrieveModelMixin,
                mixins.DestroyModelMixin,
                GenericViewSet):
    queryset = FilmImages.objects.all()
    serializer_class = FilmImagesSerializer