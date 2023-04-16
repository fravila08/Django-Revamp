# Django Validators & Tests

## Topics Covered / Goals

- Know how to write Django Validators
- Know how to create Django Tests for Models

## Lesson

So far we've been able to create a Pokemon model for our Pokedex, and this model is able to hold quite a bit of information, but, we don't have a method of validating the inputs being passed into our model.

**General steps for creating database models**

- create models
- add validators
- makemigrations
- migrate
- test models

## Adding Validators

Django has very common validators built-in to the Django Framework. [Built in validators](https://docs.djangoproject.com/en/4.1/ref/validators/#built-in-validators).

For example, if we want to validate a minimum (or maximum) integer we can use the built-in validator `MinValueValidator()`. Let's utilize this information and add some validators onto our pokemon model.

```py
# models has many different methods we will utilize when creating our Models
from django.db import models
from django.utils import timezone
# import built-in Django Validators
from django.core import validators as v

# Create your models here.
class Pokemon(models.Model):
    # CharField is a character field and has a default max length of 255 characters
    name = models.CharField(max_length=200, blank=False, null=False)
    # Adding both the min and vax value will ensure Pokemon could only go from levels 1-100
    level = models.IntegerField(default=1, validators=[v.MinValueValidator(1), v.MaxValueValidator(100)])
    # Under the hood DateField is already running a regex funciton to ensure 
	# input is matching the correct date format of "YYYY-MM-DD"
    date_encountered = models.DateField(default="2008-01-01")
    # Under the hood DateField is already running a regex funciton to ensure 
	# input is matching the correct date format of "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"
    date_captured = models.DateTimeField(default=timezone.now())
    # We don't want a pokemon's description to either be too long or too short so
    # lets add both a Max and Min LengthValidators to our TextField to ensure
    # input meets our criteria
    description = models.TextField(default="Unkown", validators=[v.MinLengthValidator(25), v.MaxLengthValidator(150)])
    # Boolean field is already ensuring to only take in either True or False
    captured = models.BooleanField(default = False)
```

> Validators will run when we run `model_instance.full_clean()` >[object validation docs](https://docs.djangoproject.com/en/4.1/ref/models/instances/#validating-objects)

We can also create our own validators...

Our pokemon model has a `name` field but we only want names to be written onto our database in a specific format. However, our `name` field allows for any combination of characters, numbers, and spaces to get entered and saved onto the database.

We can create a **validator** which is a method to check for a valid pokemon `name` input.

Let's create a new file `validators.py` inside our `pokemon_app` folder

```python
# validator.py

# This will allow us to throw a validation error when interacting with 
# our models.
from django.core.exceptions import ValidationError
# This will allow us to search through our string to match our regex function
import re


# This will allow us to throw a validation error when interacting with 
# our models.
from django.core.exceptions import ValidationError
# This will allow us to search through our string to match our regex function
import re

def validate_name(name):
    error_message = "Improper name format"
    # Message we want to give the user when passing incorrect input
    regex = r'^[A-Z][a-zA-Z]*$'
    # ^: The caret symbol denotes the start of the string.
    # [A-Z]: This matches a single capital letter at the beginning of the string.
    # [a-zA-Z]*: This matches zero or more occurrences of any alphabetic character (both uppercase and lowercase) after the first capital letter.
    # $: The dollar sign denotes the end of the string.
    good_name = re.match(regex, name)
    # returns a boolean value [True || False]
    if good_name:
        return name
    else:
        raise ValidationError(error_message, params={ 'name' : name })
```

Now we can import it and add it onto our pokemon Model.

```python
# import validate_name from our custom validators
from .validators import validate_name


# Create your models here.
class Pokemon(models.Model):
    # Takes in custom validator
    name = models.CharField(max_length=200, blank=False, null=False, validators=[validate_name])
    # Adding both the min and vax value will ensure Pokemon could only go from levels 1-100
```


## Testing Our Models

- **Using Tests**

  In our `pokemon_app` directory, inside the `tests.py` file we can write our unit tests.

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Pokemon # import pokemon model

# Create your tests here.
class pokemon_test(TestCase):
    
    def test_01_create_pokemon_instance(self):
        # Here we will create our pokemon instance
        new_studet = Pokemon(name="Pikachu", description = 'Only the best electric type pokemon in the show but NOT in the games')
        try:
            # remember validators are not ran on our new instance until we run full_clean
            new_studet.full_clean()
            # here we will ensure our instance is actually created
            self.assertIsNotNone(new_studet)
        except ValidationError as e:
            # print(e.message_dict)
            #if it sends an error we want to ensure this test fails
            self.fail()
        
    def test_02_create_pokemon_with_incorrect_name_format(self):
        # we create an instance with an improper name
        new_studet = Pokemon(name='ch4r1z4 rd', description = 'Looks like a Dragon has wings, breathes fire.. but is not a dragon')
        try:
            new_studet.full_clean()
            # if our instance runs through the full clean and doesn't throw an error, than we
            # know our validator is not working correctly and we should fail this test 
            self.fail()

        except ValidationError as e:
            # print(e.message_dict)
            # we can ensure the correct message is inside our ValidationError
            self.assertTrue('Improper name format' in e.message_dict['name'])
```

To run your tests execute the command `python manage.py test` in the terminal and we should see a . for every test or an E for error and or F for failure.


## External Resources

- [Django Docs](https://docs.djangoproject.com/en/2.2/)
- [Django Queries Cheat Sheet](https://github.com/chrisdl/Django-QuerySet-Cheatsheet)
- [Django Validators Resource](https://docs.djangoproject.com/en/2.2/ref/validators/)

## Assignments
