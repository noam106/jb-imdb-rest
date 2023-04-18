from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
import datetime
from django.core.exceptions import ValidationError
# Create your models here.


def validete_actoe_age(birth_year):
    if datetime.datetime.now().year - int(birth_year) < 5:
        raise ValidationError(" the actor is to young")


def validate_oscar_year(oscar_year: int):
    if datetime.datetime.now().year < int(oscar_year):
        raise ValidationError("you cant enter an oscar from the future")
    if int(oscar_year) < 1929:
        raise ValidationError('There was no oscar before 1929')

class Actor(models.Model):


    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    birth_year = models.IntegerField(db_column='birth_year',null=True, blank=True, validators=[validete_actoe_age])

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'actors'


class Movie(models.Model):

    name = models.CharField(max_length=256, db_column='name', null=False)
    description = models.TextField(db_column='description', null=False)
    duration_in_min = models.FloatField(db_column='duration', null=False)
    release_year = models.IntegerField(db_column='year', null=False)
    pic_url = models.URLField(max_length=512, db_column='pic_url', null=True)
    director = models.ForeignKey("Director", on_delete=models.CASCADE, null=True, blank=True)
    actors = models.ManyToManyField(Actor, through='MovieActor')

    # def __str__(self):
    #     return self.name

    class Meta:
        db_table = 'movies'


class Rating(models.Model):

    movie = models.ForeignKey(
        'Movie',
        on_delete=models.CASCADE,
    )
    rating = models.SmallIntegerField(db_column='rating', null=False,
                validators=[MinValueValidator(1), MaxValueValidator(10)])
    rating_date = models.DateField(db_column='rating_date', null=False, auto_now_add=True)


    class Meta:
        db_table = 'ratings'


class MovieActor(models.Model):
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    salary = models.IntegerField(null=True, blank=True)
    main_role = models.BooleanField(null=False, blank=False)

    def __str__(self):
        return f"{self.actor.name} in movie {self.movie.name}"


    class Meta:
        db_table = 'movie_actors'


class Oscar(models.Model):
    year = models.IntegerField(db_column='year', null=False, validators=[validate_oscar_year])
    nominations = models.CharField(max_length=256, db_column='nominations', null=False, blank=False)
    actor = models.ForeignKey(Actor, on_delete=models.CASCADE, null=True, blank=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    director = models.ForeignKey("Director", on_delete=models.CASCADE, null=True, blank=True)


class Director(models.Model):
    name = models.CharField(max_length=256, db_column='name', null=False, blank=False)
    birth_year = models.IntegerField(db_column='birth_year', null=True, blank=True, validators=[validete_actoe_age])

# class Nominations(models.Model):
#     nominations = models.CharField(max_length=256, db_column='nomination', null=False, blank=False)
#     movie = m