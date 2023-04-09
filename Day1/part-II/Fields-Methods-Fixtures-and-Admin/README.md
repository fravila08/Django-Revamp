# Fields, Methods, Fixtures, Admin

Earlier today we created a `Students` model, but we only touched the tip of the iceberg when it comes to model fields. Lets take it a step further and take a look at some useful fields, and validators.


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
## Improving our Students Model

Lets apply these fields to our student model with some default values and built in validators.


Lets take a look at our new and improved student object and what each argument means:

```python
from django.db import models
from django.utils import timezone

class Students(models.Model):
    # We don't want to provide a default value for a students name, but I want to specify that this field can't be blank nor can it be null
    name = models.CharField(max_length=200, blank=False, null=False)
    # By giving it the unique argument I'm telling my db no more than one field can have this email.
    email = models.EmailField(unique = True)
    # We are providing a default to someone born Jan 1st 2008
    date_of_birth = models.DateField(default="2008-01-01")
    # If a value is not provided we are stating the last time this student was at school was upon creation of the classes instance.
    last_time_at_school = models.DateTimeField(default=timezone.now())
    # Here I specify this point can't have more than 2 decimal points.
    daily_allowance = models.DecimalField(max_digits = 5, decimal_places = 2, default=00.00)
    # If no value is provided than the instance will be given the value of 10
    year_of_schooling = models.IntegerField(default=10)
    # If no value is provided the students description will be "Unkown"
    description = models.TextField(default="Unkown")
    # Every Student is a Good student so we will set that as a default value.
    good_student = models.BooleanField(default=True)
```

Lets enter psql and delete any prior instance of our Students Model before making our new migrations to ensure our updated fields don't conflict with any existing data.
```bash
    psql school_db
    school_db=# DELETE FROM students_app_students;
    DELETE 1
    school_db=# \q
```
Lets make migrations and enter our Django Python Shell to create a couple of new instances.
```bash
    # Migrate our updated Students Model
    python manage.py makemigrations
    python manage.py migrate

    # Enter Django Python Shell and Create new Students
    python manage.py shell
    >>> from students_app.models import Students
    >>> john = Students(name = 'John Avalos', email = 'john@gmail.com', daily_allowance = 2.50, year_of_schooling = 15, description = 'this is an amazingly bad student', good_student = False)
    >>> john.save()

    # If I print john now I'll see see a useless Students object
    >>> print(john)
    Students object (2)
    >>> exit()
```

## Adding class methods to our Models

We just saw that printing an instance returns a `Students object (#)`, but we want to be able to actually see our students details. lets add a couple of methods to our Students Model to increase it's usefullness.

```python
    # DUNDER Method
    def __str__(self):
        return f"{self.name} is in his {self.year_of_schooling} year of schooling and { 'is' if self.good_student else 'is not' } a good student!"

    # Adding the ability to increase a students allowance.
    def increase_allowance(self, amount):
        self.daily_allowance += amount
        self.save()

    # Change a students 'good_student' status to the opposite of it's current value
    def change_student_status(self):
        self.good_student = not self.good_student
        self.save()
```

We do not need to `makemigrations` for class methods, so lets go back into our Django Python Shell and test out these methods.

```python
    >>> from students_app.models import Students
    >>> students = Students.objects.all()
    >>> print(students)
    # Now we see John Avalos dunder method
    <QuerySet [<Students: John Avalos is in his 15 year of schooling and is not a good student!>]>
    # lets update his good student status and watch his dunder method change.
    >>> students[0].change_student_status()
    >>> print(students)
    # You can see the Dunder method has changed
    <QuerySet [<Students: John Avalos is in his 15 year of schooling and is a good student!>]
    # Lets add another Students instance and move onto fixtures
    >>> new_student = Students(name = 'Jimmy Fallon', email = 'jimmy@gmail.com')
    >>> new_student.save()
```

## Fixtures

When working in teams or in the development process, you may want to capture all existing data inside your projects database belonging to an app to later utilize further in case something happens to your database. This is where fixtures comes in.


Before getting into creating JSON data, lets create a `fixtures` directory inside of our 'students_app' and a `student_data.json` inside of `fixtures`

```bash
    mkdir students_app/fixtures
    touch students_app/fixtures/students_data.json
```
- Dump Data: will dump all of your data in a JSON format.

```bash 
    python manage.py dumpdata students_app.Students

    # will return an array of JSON objects with our students information
    [{"model": "students_app.students", "pk": 2, "fields": {"name": "John Avalos", "email": "john@gmail.com", "date_of_birth": "2008-01-01", "last_time_at_school": "2023-04-09T05:48:14.774Z", "daily_allowance": "2.50", "year_of_schooling": 15, "description": "this is an amazingly bad student", "good_student": true}}, {"model": "students_app.students", "pk": 3, "fields": {"name": "Jimmy Fallon", "email": "jimmy@gmail.com", "date_of_birth": "2008-01-01", "last_time_at_school": "2023-04-09T06:12:32.480Z", "daily_allowance": "0.00", "year_of_schooling": 10, "description": "Unkown", "good_student": true}}]
```
- Now copy it and paste it onto the `students_data.json`. Now you could make alterations to your database without putting it's data at risk.

- Load Data: will create an instance of a Model corresponding to the JSON object.

```bash
    python manage.py loaddata students_data.json
    Installed 2 object(s) from 1 fixture(s)
```

## Django Admin Site

So far we've utilized the Django Shell to interact with our models, and although it works, it could definitely be more useful to have a more interactive site. That's where Django admin site comes in.


First lets register our `Students Model` onto Django Admins Site.

```python
    # students_app/admin.py
    from django.contrib import admin
    # Explecit import of Students Model
    from .models import Students

    # Register your models here.
    admin.site.register([Students])
```

Now before entering our Admin Site with Django we must create a super user to log into our admin site and manipulate our models.

```bash
    python manage.py createsuperuser
    # You'll be queried to provide a username, email, and password
```

Finally we are ready to enter our Admin Site and interact with our `Students Model`.

```bash
    python manage.py runserver
```

Once your server is running, open up your browser and go to [http:localhost:8000/admin](http:localhost:8000/admin), log in and you'll have a well constructed user interface to interact with your models. Press `ctrl + C` to kill your server and return to your terminal.
