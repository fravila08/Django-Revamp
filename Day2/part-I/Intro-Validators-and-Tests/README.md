# Django Validators & Tests

## Topics Covered / Goals

- Know how to write Django Validators
- Know how to create Django Tests for Models

## Lesson

So far we've been able to create a Student model for our school, and this model is able to hold quite a bit of information that it can handle, but, we don't have anyway of validating data to ensure it's valid for our program.

**General steps for creating database models**

- create models
- add validators
- makemigrations
- migrate
- test models

## Adding Validators

Django has very common validators built-in to the Django Framework. [Built in validators](https://docs.djangoproject.com/en/4.1/ref/validators/#built-in-validators).

For example, if we want to validate a minimum (or maximum) integer we can use the built-in validator `MinValueValidator()`. Let's utilize this information and add some validators onto our Student model.

```py
## models.py
from django.db import models
from django.utils import timezone
# import built-in Django Validators
from django.core import validators as v


class Students(models.Model):
    # This will likely need a custom validator
    name = models.CharField(max_length=200, blank=False, null=False)
    # Validate Email is already running under the hood of EmailField but 
    # if I were to mannually add it to a field it would like like this
    email = models.EmailField(unique = True, validators=[v.validate_email])
    # Under the hood DateField is already running a regex funciton to ensure 
	# input is matching the correct date format of "YYYY-MM-DD"
    date_of_birth = models.DateField(default="2008-01-01")
    # Under the hood DateField is already running a regex funciton to ensure 
	# input is matching the correct date format of "YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]"
    last_time_at_school = models.DateTimeField(default=timezone.now())
    # DecimalField has it's own validator and takes the same arguments as the field itself.
    daily_allowance = models.DecimalField(max_digits=5, decimal_places=2, default=00.00, validators=[v.DecimalValidator(5, 2)])
     # Lets change this into a PositiveIntegerField since that's what we want an add an 
    # calidation to ensure only int types could be passed onto this field. Lets also add a max and 
    # min value to years of schooling.
    year_of_schooling = models.PositiveIntegerField(default=10, validators=[v.integer_validator, v.MinValueValidator(1), v.MaxValueValidator(27)])
    # We don't want a student's description to either be too long or too short so
    # lets add both a Max and Min LengthValidators to our TextField to ensure
    # input meets our criteria
    description = models.TextField(validators=[v.MaxLengthValidator(500), v.MinLengthValidator(50)])
    # Boolean field is already ensuring to only take in either True or False
    good_student = models.BooleanField(default=True)
```

> Validators will run when we run `model_instance.full_clean()` >[object validation docs](https://docs.djangoproject.com/en/4.1/ref/models/instances/#validating-objects)

We can also create our own validators...

Our Student model has a `name` field but we only want names to be written onto our database in a specific format. However, our `name` field allows for any combination of letters names and spaces to get entered and saved into the database.

We can create a **validator** which is a method to check for a valid locker `name` input.

Let's create a new file `validators.py` inside our `student_app` folder

```python
# validator.py

# This will allow us to throw a validation error when interacting with 
# our models.
from django.core.exceptions import ValidationError
# This will allow us to search through our string to match our regex function
import re


def validate_name(name):
    error_message = "Improper name format please enter First and Last seperated by a space and with proper capitalization"
    # Message we want to give the user when passing incorrect input
    regex = r'^[A-Z][a-z]+( [A-Z][a-z]+)*$'
    # ^ matches the start of the string.
    # [A-Z] matches a single uppercase letter.
    # [a-z]+ matches one or more lowercase letters.
    # ( [A-Z][a-z]+)* matches zero or more occurrences of a space followed by an uppercase letter and one or more lowercase letters.
    # $ matches the end of the string.
    good_name = re.match(regex, name)
    # returns a boolean value [True || False]
    if good_name:
        return name
    else:
        raise ValidationError(error_message, params={ 'name' : name })
```

Now we can import it and add it onto our Student Model.

```python
	# importing custom Validators
from .validators import validate_name


class Students(models.Model):
    # This will likely need a custom validator
    name = models.CharField(max_length=200, blank=False, null=False, validators=[validate_name])
```


## Testing Our Models

- **Using Tests**

  In our `student_app` directory, inside the `tests.py` file we can write our unit tests.

```python
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Students # import Student model

# Create your tests here.
class student_test(TestCase):
    
    def test_01_create_student_instance(self):
        # Here we will create our Student instance
        new_studet = Students(name="Nick Cage", email="nick@gmail.com", year_of_schooling=2, description="Nick Cage is an excellent student that gives his classes everything he can all the time every time.")
        try:
            # remember validators are not ran on our new instance until we run full_clean
            new_studet.full_clean()
            # here we will ensure our instance is actually created
            self.assertIsNotNone(new_studet)
        except ValidationError as e:
            # print(e.message_dict)
            #if it sends an error we want to ensure this test fails
            self.fail()
        
    def test_02_create_student_with_incorrect_name_format(self):
        # we create an instance with an improper name
        new_studet = Students(name='pancho 23 V1lla', email='pancho@gmail.com', description="Panch was an ok student that his best but really struggled.")
        try:
            new_studet.full_clean()
            # if our instance runs through the full clean and doesn't throw an error, than we
            # know our validator is not working correctly and we should fail this test 
            self.fail()

        except ValidationError as e:
            # print(e.message_dict)
            # we can ensure the correct message is inside our ValidationError
            self.assertTrue('Improper name format please enter First and Last seperated by a space and with proper capitalization' in e.message_dict['name'])
```

To run your tests execute the command `python manage.py test` in the terminal and we should see a . for every test or an E for error and or F for failure.


## External Resources

- [Django Docs](https://docs.djangoproject.com/en/2.2/)
- [Django Queries Cheat Sheet](https://github.com/chrisdl/Django-QuerySet-Cheatsheet)
- [Django Validators Resource](https://docs.djangoproject.com/en/2.2/ref/validators/)

## Assignments
