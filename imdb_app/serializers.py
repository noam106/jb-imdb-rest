from rest_framework import serializers

from imdb_app.models import *



# class MovieSerializer(serializers.Serializer):
#
#     name = serializers.CharField()
#     release_date = serializers.IntegerField()
#     dscription = serializers.CharField()
#
# m = Movie()
# ser = MovieSerializer(m)
# ser.data

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = '__all__'

class DetailedMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        exclude = ['actors']

class ActorsInMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieActor
        # fields = '__all__'
        exclude = ['id', 'movie']
        depth = 1


class RatingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        fields = ['rating', 'rating_date']


class RatingsMovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rating
        # depth = 1
        fields = ['rating', 'rating_date']


class CreateMovieSerializer(serializers.Serializer):

    release_year = serializers.IntegerField(
        validators=[MinValueValidator(1800)]
    )
    class Meta:
        model = Movie
        fields = ['id', 'name', 'description', 'duration_in_min', 'release_year']
        # לתת ארגיומנטים לפרמטר ספציפי אפשר להעביר כמה על כל פרמטר
        extra_kwargs = {
            'id': {'read_only': True}
        }

class CreateActorSerializers(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ['id','name', 'birth_year']
        extra_kwargs = {"id" : {"read_only": True},
                        "birth_year": {'required': False}
        }

class CreateRatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True}}
# class ActorManageSerializers(serializers.ModelSerializer):
#
#     class Meta:
#         modle = Actor

class CreateMovieActorSerializers(serializers.ModelSerializer):

    class Meta:
        model = MovieActor
        fields = '__all__'
        extra_kwargs = {"id": {"read_only": True},
                        "salary": {'required': False}
                        }

class UpdateMovieActor(serializers.ModelSerializer):

    class Meta:
        model = MovieActor
        fields = "__all__"
        extra_kwargs = {"id": {"read_only": True}}

