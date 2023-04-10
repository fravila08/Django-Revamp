from django.db import models
from django.core import validators as v


# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=100, validators=[v.MinLengthValidator(5)])
    
    def __str__(self):
        return self.name
