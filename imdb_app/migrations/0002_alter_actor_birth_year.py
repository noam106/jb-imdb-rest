# Generated by Django 4.1.7 on 2023-04-03 17:16

from django.db import migrations, models
import imdb_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('imdb_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='actor',
            name='birth_year',
            field=models.IntegerField(blank=True, db_column='birth_year', null=True, validators=[imdb_app.models.validete_actoe_age]),
        ),
    ]
