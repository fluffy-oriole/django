from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from films.models import Film
from films.serializers import FilmSerializer



class FilmsViewset(mixins.ListModelMixin, GenericViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer