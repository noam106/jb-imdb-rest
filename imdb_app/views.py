import os
from django.db.models import Avg
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.shortcuts import render, get_object_or_404
from imdb_app.models import *
from imdb_app.serializers import *

# Create your views here.


@api_view(['GET'])
def get_movies(request: Request):
    all_movies = Movie.objects.all()
    print("initial query:", all_movies.query)

    if 'name' in request.query_params:
        all_movies = all_movies.filter(name__iexact=request.query_params['name'])
        print("after adding name filter", all_movies.query)
    if 'duration_from' in request.query_params:
        all_movies = all_movies.filter(duration_in_min__gte=request.query_params['duration_from'])
        print("after adding duration_from filter", all_movies.query)
    if 'duration_to' in request.query_params:
        all_movies = all_movies.filter(duration_in_min__lte=request.query_params['duration_to'])
        print("after adding duration_to filter", all_movies.query)
    if 'description' in request.query_params:
        all_movies = all_movies.filter(description__icontains=request.query_params['description'])
        print("after adding description filter", all_movies.query)

    serializer = MovieSerializer(instance=all_movies, many=True)
    return Response(data=serializer.data)
# @api_view(['GET'])
# def get_movies(request):
#     return Response(data={'movies': 'hello'})


@api_view(['GET', 'POST'])
def get_actor(request: Request):
    if request.method == "GET":
        all_actors = Actor.objects.all()
        serializer = ActorSerializer(instance=all_actors, many=True)
        return Response(serializer.data)
    else:
        serializer = CreateActorSerializers(data=request.data)
        # print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    serializer = DetailedMovieSerializer(instance=movie)
    return Response(data=serializer.data)


@api_view(['GET'])
def get_actor_in_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    all_cast = movie.movieactor_set.all()
    serializer = ActorsInMovieSerializer(instance=all_cast, many=True)
    return Response(data=serializer.data)


@api_view(["DELETE", 'PUT', 'PATCH'])
def delete_actor_from_movie(request, movie_id, actor_id):
    # movie = get_object_or_404(Movie, id=movie_id)
    # actor = get_object_or_404(Actor, id=actor_id)
    movie_actor_obj = get_object_or_404(MovieActor, movie_id=movie_id, actor_id=actor_id)
    movie_actor_obj.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['PUT', 'PATCH'])
def update_actor_from_movie(request, movie_id, actor_id):
    # movie = get_object_or_404(Movie, id=movie_id)
    # actor = get_object_or_404(Actor, id=actor_id)
    movie_actor_obj = get_object_or_404(MovieActor, movie_id=movie_id, actor_id=actor_id)
    serializer = CreateMovieActorSerializers(instance=movie_actor_obj, data=request.data, partial=request.method == 'PATCH')
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data)


@api_view(["POST"])
def add_actor_to_movie(request, movie_id):
    print(request.data)
    movie = get_object_or_404(Movie, id=movie_id)
    # to chack
    postman_data = request.data(mutable=True)
    postman_data.objects.movie_id = movie
    print(postman_data)
    actor_id = postman_data['actor_id']
    print(actor_id)
    actor = get_object_or_404(Actor, id=actor_id)
    postman_data['movie_id'] = [movie.id]
    print(postman_data)
    serializer = CreateMovieActorSerializers(data=postman_data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=postman_data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_ratings_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    all_ratings = movie.rating_set.all()
    serializer = RatingsMovieSerializer(instance=all_ratings, many=True)

    return Response(data=serializer.data)


@api_view(['GET'])
def get_movie_rating_avg(request, movie_id):
    avg_rating = get_object_or_404(Movie, id=movie_id).rating_set.aggregate(Avg('rating'))
    return Response(avg_rating)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def get_actor_by_id(request, actor_id: int):
    actor = get_object_or_404(Actor, id=actor_id)
    if request.method == 'GET':
        serializer = CreateActorSerializers(instance=actor)
        return Response(serializer.data)
    elif request.method in ('PUT', 'PATCH'):
        serializer = CreateActorSerializers(instance=actor, data=request.data, partial=request.method == 'PATCH')
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data)
    else:
        actor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_all_ratings(request):
    all_ratings = Rating.objects.all()
    if 'start_date' in request.data and 'end_date' in request.data:
        if request.data['start_date'] >= request.data['end_data']:
            return Response('check your dates somthing isnt right', status=status.HTTP_406_NOT_ACCEPTABLE)
        else:
            all_ratings = all_ratings.filter(rating_date__range=(request.data['start_date'],
                                                                 request.data['end_date']))
            serializer = RatingsSerializer(instance=all_ratings, many=True)
            return Response(data=serializer.data)
    serializer = RatingsSerializer(instance=all_ratings, many=True)
    return Response(data=serializer.data)


@api_view(['POST'])
def add_rating_to_movie(request, movie_id: int):
    serializer = CreateRatingSerializers(data=request.data)
    # print(request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def delete_raing(request, rating_id):
    rating = get_object_or_404(Actor, id=rating_id)
    rating.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)