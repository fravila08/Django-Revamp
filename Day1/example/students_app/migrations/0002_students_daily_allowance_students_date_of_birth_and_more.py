# Generated by Django 4.2 on 2023-04-09 05:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('students_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='daily_allowance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='students',
            name='date_of_birth',
            field=models.DateField(default='2008-01-01'),
        ),
        migrations.AddField(
            model_name='students',
            name='description',
            field=models.TextField(default='Unkown'),
        ),
        migrations.AddField(
            model_name='students',
            name='good_student',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='students',
            name='last_time_at_school',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 9, 5, 47, 11, 569409, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AddField(
            model_name='students',
            name='year_of_schooling',
            field=models.IntegerField(default=10),
        ),
    ]