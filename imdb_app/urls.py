"""imdb_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from imdb_app import views
from imdb_app.viwe_set import ActorViewSet, OscarViewSet, MovieViewSet, DirectorViewSet

router = DefaultRouter()
router.register('actors', ActorViewSet)
router.register('movies', MovieViewSet)
router.register('oscar', OscarViewSet)
router.register('director', DirectorViewSet)

urlpatterns = [
    path('movies', views.get_movies),
    path('actors', views.get_actor),
    path('movie/<int:movie_id>', views.get_movie),
    path('movie/<int:movie_id>/actors', views.get_actor_in_movie),
    path('ratings', views.get_all_ratings),
    path('movie/<int:movie_id>/rating', views.get_ratings_movie),
    path('movie/<int:movie_id>/rating/average', views.get_movie_rating_avg),
    path('actor/<int:actor_id>', views.get_actor_by_id),
    path('movie/<int:movie_id>/delete/<int:actor_id>', views.delete_actor_from_movie),
    path('movie/<int:movie_id>/actor', views.add_actor_to_movie),
    path('movie/<int:movie_id>/update/<int:actor_id>', views.update_actor_from_movie),
    path('rating/<int:movie_id>', views.add_rating_to_movie),
    path('rating/delete/int: rating_id', views.delete_raing),

]
urlpatterns.extend(router.urls)