from django.db import models
from django.core import validators as v
from django.core.exceptions import ValidationError
from .validators import validate_move_name

# Create your models here.


class Move(models.Model):
    # We could use the same validator we created for the Pokemon Name for our Moves Name
    name = models.CharField(max_length=250, blank=False,
                            null=False, validators=[validate_move_name])
    # We want each move to have an accuracy between 1 and 100 percent and we will give it a default of 70%
    accuracy = models.PositiveIntegerField(
        default=70, validators=[v.MinValueValidator(1), v.MaxValueValidator(100)])
    # Each move has a max Power Point representation that we could increase with special items
    maxPP = models.IntegerField(
        default=20, validators=[v.MinValueValidator(5),v.MaxValueValidator(30)])
    # We want each move to have PP between 0 if they've utilized this move too much and 30 depending on it's max capability
    pp = models.IntegerField(default=20, validators=[
                             v.MinValueValidator(1)])
    # We want to know just how much Power each move has
    power = models.PositiveIntegerField(
        default=80, validators=[v.MaxValueValidator(120)])

    def __str__(self):
        return f"| {self.name} | accuracy: {self.accuracy} | power: {self.power} | current_pp: {self.pp}/{self.maxPP} |"

    def increase_max_pp(self, increment):
        self.maxPP = self.maxPP + increment
        self.save()

    # Lets ensure that when clean is ran against our Model we check that PP is not greater than Max PP
    def clean(self):
        if self.pp > self.maxPP:
            raise ValidationError("PP can't be higher than Max PP")