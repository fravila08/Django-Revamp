# Fields, Methods, Fixtures, Admin

Earlier today we created a `Pokemon` model, but we only touched the tip of the iceberg when it comes to model fields. Lets take it a step further and take a look at some useful fields, and validators.


## Useful Model Fields

```python
# utilize timezone for any Django Date/DateTime/TZ fields since it already provides 
# the correct format

# DateField will accept a date in the following format "YYYY-MM-DD"
date_of_birth = models.DateField()

#DateTimeField will accept a data, time, and timezone in the following format "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ] format."
last_time_at_school = models.DateTimeField()

# DecimalField will take in decimal numbers and you can specify how many decimal places
# are allowed and/or how many overall digits are allowed.
daily_allowance = models.DecimalField(decimal_places = 2)

# IntegerField will take in whole numbers only but does not care if integer holds a positive or negatice value if you want only positive integers utilize PositiveIntegerField
year_of_schooling = models.IntegerField()


# TextField, unlike CharField TextField does not have any maximum character count.
description = models.TextField()

# BooleanField will take in boolean values only
good_student = models.BooleanField()

```
## Improving our Pokemon Model

Lets apply these fields to our student model with some default values and built in validators.


Lets take a look at our new and improved student object and what each argument means:

```python
from django.db import models
from django.utils import timezone

# Create your models here.
# models.Model tell Django this is a Model that should be reflected on our database
class Pokemon(models.Model):
    # CharField is a character field and has a default max length of 255 characters
    name = models.CharField(max_length=200, blank=False, null=False)
    # IntegerField will allow only solid numerical values as input
    level = models.IntegerField(default=1)
    # We are providing a default to someone born Jan 1st 2008
    date_encountered = models.DateField(default="2008-01-01")
    # If a value is not provided we are stating the last time this student was at school was upon creation of the classes instance.
    date_captured = models.DateTimeField(default=timezone.now())
    # If no value is provided the Pokemon description will be "Unkown"
    description = models.TextField(default="Unkown")
    # We must catch them all.
    captured = models.BooleanField(default = False)
```

Lets make migrations and enter our Django Python Shell to create a couple of new instances.

```bash
    # Migrate our updated Pokemon Model
    python manage.py makemigrations
    python manage.py migrate

    # Enter Django Python Shell and Create new Pokemon
    python manage.py shell
    >>> from pokemon_app.models import Pokemon
    >>> charizard = Pokemon(name = 'Charizard', level = 25, date_encountered = "2007-04-07", captured = True)
    >>> charizard.save()

    # If I print john now I'll see see a useless Pokemon object
    >>> print(john)
    Pokemon object (2)
    >>> exit()
```

## Adding class methods to our Models

We just saw that printing an instance returns a `Pokemon object (#)`, but we want to be able to actually see our Pokemon details. lets add a couple of methods to our Pokemon Model to increase it's usefullness.

```python
    # DUNDER METHOD
    def __str__(self):
        return f"{self.name} {'has been captured' if self.captured else 'is yet to be caught'}"
    
    # RAISES POKEMON'S LEVEL
    def level_up(self):
        self.level += 1
        self.save()
        
    # Switches Pokemon's captured status from True to False and vise versa
    def change_caught_status(self):
        self.captured = not self.captured
        self.save()
```

We do not need to `makemigrations` for class methods, so lets go back into our Django Python Shell and test out these methods.

```python
    >>> from pokemon_app.models import Pokemon
    >>> pokemon = Pokemon.objects.all()
    >>> print(pokemon)
    # Now we see John Avalos dunder method
    <QuerySet [<Pokemon: Pikachu is yet to be caught>, <Pokemon: Charizard has been captured>]>
    # lets update his good student status and watch his dunder method change.
    >>> pokemon[0].change_caught_status()
    >>> print(pokemon)
    # You can see the Dunder method has changed
    <QuerySet [<Pokemon: Charizard has been captured>, <Pokemon: Pikachu has been captured>]>
    # Lets add another Pokemon instance and move onto fixtures
    >>> blastoise = Pokemon(name = 'Blastoise', level = 37)
    >>> blastoise.save()
```

## Fixtures

When working in teams or in the development process, you may want to capture all existing data inside your projects database belonging to an app to later utilize further in case something happens to your database. This is where fixtures comes in.


Before getting into creating JSON data, lets create a `fixtures` directory inside of our 'Pokemon_app' and a `pokemon_data.json` inside of `fixtures`

```bash
    mkdir pokemon_app/fixtures
    python manage.py dumpdata pokemon_app.Pokemon --indent 2 > pokemon_app/fixtures/pokemon_data.json
```
- You'll see that dumpdata created a new json file inside the fixtures directory 

```json
    # Will display each Pokemon Instance in json format
[
    {
        "model": "pokemon_app.pokemon",
        "pk": 1,
        "fields": {
            "name": "Pikachu",
            "level": 12,
            "date_encountered": "2008-01-01",
            "date_captured": "2023-04-14T05:16:41.794Z",
            "description": "Unkown",
            "captured": true
        }
    }
]
```

- Load Data: will create an instance of a Model corresponding to the JSON object.

```bash
    python manage.py loaddata pokemon_data.json
    Installed 3 object(s) from 1 fixture(s)
```

## Django Admin Site

So far we've utilized the Django Shell to interact with our models, and although it works, it could definitely be more useful to have a more interactive site. That's where Django admin site comes in.


First lets register our `Pokemon Model` onto Django Admins Site.

```python
    # Pokemon_app/admin.py
    from django.contrib import admin
    # Explecit import of Pokemon Model
    from .models import Pokemon

    # Register your models here.
    admin.site.register([Pokemon])
```

Now before entering our Admin Site with Django we must create a super user to log into our admin site and manipulate our models.

```bash
    python manage.py createsuperuser
    # You'll be queried to provide a username, email, and password
```

Finally we are ready to enter our Admin Site and interact with our `Pokemon Model`.

```bash
    python manage.py runserver
```

Once your server is running, open up your browser and go to [http:localhost:8000/admin](http:localhost:8000/admin), log in and you'll have a well constructed user interface to interact with your models. Press `ctrl + C` to kill your server and return to your terminal.
