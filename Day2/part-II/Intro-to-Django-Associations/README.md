# Django Associations

## Lesson

So far we've created a well constructed Students model in our student_app for every student in a school. Now we need to create a `School` model for students to be able to attend. Just like in OOP we want to try and keep the `single responsibility principle` with our apps meaning that each app should do only ONE thing and do it WELL.

## Creating our School App and Model

Lets quickly create a `school_app` and `school` model to interact with our students.

```bash
	# create our app
	python manage.py createapp school_app
```

Lets quickly add our school_app into `INSTALLED_APPS` in our school/settings.py

```python
	# school/settings.py
	INSTALLED_APPS = [
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
		'students_app',
		'school_app',
	]
```
Finally lets create a `School` model in school_app/models.py

```python
# school_app/models.py
from django.db import models
from django.core import validators as v

# Create your models here.
class School(models.Model):
    name = models.CharField(max_length=100, validators=[v.MinLengthValidator(5)])

	def __str__(self):
        return self.name
```

Now we can makemigrations and migrate this model.

```bash
	python manage.py makemigrations
	python manage.py migrate
```

Lets create tests for both proper and improper input

```python
#school_app/tests.py
from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import School

# Create your tests here.
class school_test(TestCase):
    
    def test_01_create_school_instance(self):
        new_school = School(name = 'Code Platoon')
        try:
            new_school.full_clean()
            self.assertIsNotNone(new_school)
        except ValidationError as e:
            # print(e.message_dict)
            self.fail()
        
    def test_02_create_school_with_incorrect_name_length(self):
        new_school = School(name='Nope')
        try:
            new_school.full_clean()
            self.fail()
        except ValidationError as e:
            # print(e.message_dict)
            self.assertTrue('Ensure this value has at least 5 characters (it has 4).' in e.message_dict['name'])
```

To end this process lets utitlize the Django python shell to create a school to make relationships with.

```bash
	# enter shell
	python manage.py shell
	# in python shell
	>>> from school_app.models import School
	>>> code_platoon = School(name = 'Code Platoon')
	>>> code_platoon.save()
	>>> exit()
```

Perfect, now we have a Students Model and a School Model with a School instance. Lets create some associations!

## Creating our Association

As with database schema design, we can create relationships between our Django models to reflect certain requirements. Django provides some model fields to make achived this task much simpler:

- models.OneToOneField()
- models.ForiengKeyField() "many to one"
- models.ManyToManyField()

Let's take a look at how we could create a foreign key relationship between our Students Model and our School Model:

```python
# students_app/models.py

from school_app.models import School
# Import the school model for us to make a relationship with

class Students(models.Model):
	#prior fields would go here and at the bottom of our model we would add any and all associations
	school = models.ForeignKey(School, on_delete = models.CASCADE, default = 1)
	# Creating a MANY Students to ONE School relationship and setting Code Platoon as the default value
```

Now lets makemigrations and migrate.

```bash
	python manage.py makemigrations
	python manage.py migrae
```
Now lets take a look at all students and see what has changed.

```bash
	psql school_db
	school_db=# select * from students_app_students;
```

At the end of our datatable we will see a new field named school_id and for all existing instances it holds the value of 1 which is the id for `Code Platoon`.

Notice that if you run your current tests you will get an error with the message of `school instance with id 1 does not exist.` coming from `test_01_create_student_instance`. This is because our tests create their own database run our logic and then destroy that informtion. Lets fix it.

```python
	#student_app/tests.py

	from school_app.models import School
	#use the setUp method to create data that will be utilized through the entire test class
	class student_test(TestCase):
    
		def setUp(self):
			# Create a new School
			new_school = School(name = 'Code Platoon')
			new_school.save()
```
Now your tests will pass!

This is amazing, but lets practice creating a ManyToMany relationship by creating an `Exchange_Student` model where many exchange students can belong to many schools. An exchange student is still just a Students so lets add it onto our student_app.

```python
	# student_app/models.py

	# Lets utilize inheritance to utilize all of our Students Models fields
	class Exchange_Student(Students):
		# Now we could simply add a field to our Exchange_Student model
		other_schools = models.ManyToManyField(School, related_name = 'students')
		 # the related fields argument creates the ability for the School model to grab this field 
    	# through exchange_students
```

Lets create our new test for this `Exchange_Student` model.

```python 
	# student_app/tests.py
	from .models import Students, Exchange_Student

	def test_03_create_exchange_student(self):
        # Here we can create an exchange student
        exchange_stud = Exchange_Student(name="Nick Cage", email="nick@gmail.com", year_of_schooling=2, description="Nick Cage is an excellent student that gives his classes everything he can all the time every time.", school = School.objects.all().first())
        # Now we need to save our student in order to be able to access it's manyTomany relationships
        exchange_stud.save()
        # Many to many relationships are treated as sets in python so now we utilize the add function to place ids into this field
        exchange_stud.other_schools.add(6)
        try:
            exchange_stud.full_clean()
            self.assertIsNotNone(exchange_stud)
        except ValidationError as e:
            print(e.message_dict)
            self.fail()
```

Congratulations we have successfully  created and tested our Django Models. Lets register our models onto the admin site

```python
	#school_app/admin
	from .models import School

	admin.site.register([School])
	
	#students_app/admin
	from .models import Students, Exchange_Student

	admin.site.register([Students, Exchange_Student])
```
run the server

```python
	python manage.py runserver
```
and interact with our Models through the [Admin Site](http://localhost:800/admin)


