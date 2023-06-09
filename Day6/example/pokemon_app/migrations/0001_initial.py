# Generated by Django 4.2 on 2023-04-19 06:33

import datetime
import django.core.validators
from django.db import migrations, models
import pokemon_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('move_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pokemon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, validators=[pokemon_app.validators.validate_name])),
                ('level', models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100)])),
                ('date_encountered', models.DateField(default='2008-01-01')),
                ('date_captured', models.DateTimeField(default=datetime.datetime(2023, 4, 19, 6, 33, 27, 974745, tzinfo=datetime.timezone.utc))),
                ('description', models.TextField(default='This is a pokemon of a certain pokemon type that will hopefully evolve', validators=[django.core.validators.MinLengthValidator(25), django.core.validators.MaxLengthValidator(150)])),
                ('captured', models.BooleanField(default=False)),
                ('moves', models.ManyToManyField(default=[1], to='move_app.move')),
            ],
        ),
    ]
