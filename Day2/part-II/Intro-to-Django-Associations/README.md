# Django Associations

## Lesson

So far we've created a pokemon model in our pokemon_app for every pokemon in a Pokedex. Now we need to create a `Moves` model for pokemon. Just like in OOP we want to try and keep the `single responsibility principle` with our apps, meaning that each app should do only ONE thing and do it WELL.

## Creating our Moves App and Model

Lets quickly create a `move_app` and `Move` model to interact with our pokemon.

```bash
	# create our app
	python manage.py startapp move_app
```

Lets quickly add our move_app into `INSTALLED_APPS` in our pokedex_proj/settings.py

```python
	# pokedex_proj/settings.py
	INSTALLED_APPS = [
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'pokemon_app',
		'move_app',
	]
```
Now lets create a `move` model in move_app/models.py and add a couple of validators.

```python
# move_app/models.py

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

# move_app/validators.py
from django.core.exceptions import ValidationError
import re

def validate_move_name(name):
    regex = r"^[a-zA-Z]+ ?[a-zA-Z]+$"
    good_name = re.match(regex, name)
    if good_name:
        return name
    raise ValidationError("Improper Format")
```

Now we can makemigrations and migrate this model.

```bash
	python manage.py makemigrations
	python manage.py migrate
```

Lets create tests for both proper and improper input

```python
#move_app/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Move

# Create your tests here.


class move_test(TestCase):

    def test_01_create_move_instance(self):
        new_move = Move(name='Psychic')
        try:
            new_move.full_clean()
            self.assertIsNotNone(new_move)
        except ValidationError as e:
            # print(e.message_dict)
            self.fail()

    def test_02_create_move_with_incorrect_name_and_PP(self):
        new_move = Move(name='wing 4ttack', maxPP=20, pp=25)
        try:
            new_move.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assertTrue(
                'Improper Format' in e.message_dict['name'] and "PP can't be higher than Max PP" in e.message_dict['__all__'])
```

To end this process lets utitlize the Django python shell to create a move to make relationships with.

```bash
	# enter shell
	python manage.py shell
	# in python shell
	>>> from move_app.models import Move
	>>> psychic = Move(name = 'Psychic')
	>>> psychic.save()
	>>> exit()
```

Perfect, now we have a pokemon Model and a move Model with a move instance. Lets create some associations!

## Creating our Association

As with database schema design, we can create relationships between our Django models to reflect certain requirements. Django provides some model fields to make achived this task much simpler:

- models.OneToOneField()
- models.ForiengKeyField() "many to one"
- models.ManyToManyField()

Let's take a look at how we could create a Many-To-Many relationship between our Pokemon Model and our Move Model:

```python
# pokemon_app/models.py

from move_app.models import Move
# Import the move model for us to make a relationship with

class pokemon(models.Model):
	#prior fields would go here and at the bottom of our model we would add any and all associations
	moves = models.ManyToManyField(Move, default=[1])
	# Creating a MANY pokemon to ONE move relationship and setting Code Platoon as the default value

	# Lets ensure the clean method checks that we can only learn 4 moves
	def clean(self):
        if self.moves.count() > 4:  # Change the maximum number of relationships as needed
                raise ValidationError("A Pokemon can have at most 4 moves.")
```

Now lets makemigrations and migrate.

```bash
	python manage.py makemigrations
	python manage.py migrae
```
This many to many field that we have included will not be reflected in PostgreSQL, instead this relationships will be handled by Django itself and will allow you to see these relationships by using the Django query API. 

```python
pokemon = Pokemon.objects.get(id=1)  # Retrieve a Pokemon object
moves = pokemon.moves.all() # Returns a set of related Moves
<QuerySet [<Move: | Psychic | accuracy: 70 | power: 80 | current_pp: 20/20 |>]>
```
Many to Many relationships are treated as sets, meaning to add or remove from the set we must utilize the `add` or `remove` methods.

Congratulations we have successfully  created and tested our Django Models. Lets register our models onto the admin site

```python
	#move_app/admin
	from .models import Move

	admin.site.register([Move])
```
run the server

```python
	python manage.py runserver
```
and interact with our Models through the [Admin Site](http://localhost:800/admin)


