# Generated by Django 4.2 on 2023-04-10 02:59

import datetime
import django.core.validators
from django.db import migrations, models
import re
import students_app.validators


class Migration(migrations.Migration):

    dependencies = [
        ('students_app', '0003_alter_students_daily_allowance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='last_time_at_school',
            field=models.DateTimeField(default=datetime.datetime(2023, 4, 10, 2, 59, 1, 905071, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='students',
            name='name',
            field=models.CharField(max_length=200, validators=[students_app.validators.validate_name]),
        ),
        migrations.AlterField(
            model_name='students',
            name='year_of_schooling',
            field=models.PositiveIntegerField(default=10, validators=[django.core.validators.RegexValidator(re.compile('^-?\\d+\\Z'), code='invalid', message='Enter a valid integer.'), django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(27)]),
        ),
    ]
