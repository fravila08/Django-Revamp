# Generated by Django 4.2 on 2023-04-16 06:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_app', '0009_alter_pokemon_date_captured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='date_captured',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 16, 6, 6, 28, 752613, tzinfo=datetime.timezone.utc)),
        ),
    ]
