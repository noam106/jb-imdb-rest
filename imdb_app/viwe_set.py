import django_filters
from django_filters import FilterSet
from rest_framework import mixins
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from imdb_app.models import Movie, Actor, Director, Oscar
from imdb_app.serializers import ActorSerializer, MovieSerializer, DirectorSerializers, OscarSerializers


class MovieFilterSet(FilterSet):

    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    duration_from = django_filters.NumberFilter('duration_in_min', lookup_expr='gte')
    duration_to = django_filters.NumberFilter('duration_in_min', lookup_expr='lte')
    description = django_filters.CharFilter(field_name='description', lookup_expr='icontains')

    class Meta:
        model = Movie
        fields = ['release_year']


class ActorFilterSet(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    born_before = django_filters.NumberFilter('birth_year', lookup_expr='lte')
    born_after = django_filters.NumberFilter('birth_year', lookup_expr='gte')


class DirectorFilterSet(FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='iexact')
    born_before = django_filters.NumberFilter('birth_year', lookup_expr='lte')
    born_after = django_filters.NumberFilter('birth_year', lookup_expr='gte')


class OscarFilterSet(FilterSet):
    year = django_filters.CharFilter(field_name='year', lookup_expr='iexact')
    from_year = django_filters.NumberFilter(field_name='year', lookup_expr='gte')
    to_year = django_filters.NumberFilter(field_name= 'year', lookup_expr='lte')
    nomination = django_filters.CharFilter(field_name='nominations', lookup_expr='iexact')





class MovieViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):

    serializer_class = MovieSerializer
    queryset = Movie.objects.all()
    # pagination_class = MoviePageClass
    filterset_class = MovieFilterSet


class ActorViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = ActorSerializer
    queryset = Actor.objects.all()
    filterset_class = ActorFilterSet


class DirectorViewSet(mixins.CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin,
                      mixins.ListModelMixin,
                      GenericViewSet):
    serializer_class = DirectorSerializers
    queryset = Director.objects.all()
    filterset_class = DirectorFilterSet


class OscarViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   GenericViewSet):
    serializer_class = OscarSerializers
    queryset = Oscar.objects.all()