# Generated by Django 4.2 on 2023-04-19 07:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='date_captured',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 19, 7, 50, 38, 445139, tzinfo=datetime.timezone.utc)),
        ),
    ]
