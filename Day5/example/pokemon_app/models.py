# models has many different methods we will utilize when creating our Models
from django.db import models
from django.utils import timezone
# import built-in Django Validators
from django.core import validators as v
from django.core.exceptions import ValidationError
# import validate_name from our custom validators
from .validators import validate_name
from move_app.models import Move


# Create your models here.
class Pokemon(models.Model):
    # Takes in custom validator
    name = models.CharField(max_length=200, blank=False,
                            null=False, validators=[validate_name])
    # Adding both the min and vax value will ensure Pokemon could only go from levels 1-100
    level = models.IntegerField(default=1, validators=[
                                v.MinValueValidator(1), v.MaxValueValidator(100)])
    # Under the hood DateField is already running a regex funciton to ensure
    # input is matching the correct date format of "YYYY-MM-DD"
    date_encountered = models.DateField(default="2008-01-01")
    # Under the hood DateField is already running a regex funciton to ensure
    # input is matching the correct date format of "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"
    date_captured = models.DateTimeField(default=timezone.now())
    # We don't want a pokemon's description to either be too long or too short so
    # lets add both a Max and Min LengthValidators to our TextField to ensure
    # input meets our criteria
    description = models.TextField(default="This is a pokemon of a certain pokemon type that will hopefully evolve", validators=[
                                   v.MinLengthValidator(25), v.MaxLengthValidator(150)])
    # Boolean field is already ensuring to only take in either True or False
    captured = models.BooleanField(default=False)
    # Lets create a many-to-many relationship with moves with a default to the move Psychic
    moves = models.ManyToManyField(Move, default=[1])

    # DUNDER METHOD
    def __str__(self):
        return f"{self.name} {'has been captured' if self.captured else 'is yet to be caught'}"

    # RAISES POKEMON'S LEVEL
    def level_up(self, new_level):
        self.level = new_level
        self.save()

    # Switches Pokemon's captured status from True to False and vise versa
    def change_caught_status(self, status):
        self.captured = status
        self.save()

    def clean(self):
        if self.moves.count() > 4:  # Change the maximum number of relationships as needed
            raise ValidationError("A Pokemon can have at most 4 moves.")
