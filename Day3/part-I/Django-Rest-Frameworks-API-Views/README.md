# Django API Views with Django Rest Frameworks

## Lesson

So far we've created Students, Exchange_Student, and School Models utilizing Django-ORM with associations, validators, and tests. Although it's been great we still haven't talked about why we are utilizing Django-ORM to interact with our database. Django is a powerful Back-End framework that we will utilize to host our Application Programming Interface for our Full-Stack-Applications. Today we are going to begin creating `views` to interact with our models and return the data we desire.

## Things to consider when creating our API Views

1. Using JSON format for sending and receiving data.
    - This is becuase most Frameworks now a days Front-End or Back-end have built in methods to be able to effectively utilize JSON data. JSON was specifically made to interact with JavaScript and is therefor easily interpreted by JavaScript. Python has a built in method like json.loads() to grab the JSON data in the body of a request and turn it into something Python can utilize.
2. Use Filtering, Sorting, and Pagination to Retrieve the Data Requested.
    -   Databases can get very large and complicated so it's important to only grab the neccessary data from our database and sort it to create consistency in our API responses.

## Creating our first API views

To create our API views we will utilize [django-rest-frameworks](https://www.django-rest-framework.org/) to interact with our requests and deliver effective responses.

First lets create a view that will get all of our existing schools, here's an example of what we would expect it to look:

```js
{'schools': [{'id': 1, 'name': 'Code Platoon'}, {'id': 2, 'name': 'Code Academy'}]}
```
Lets install [django-rest-frameworks](https://www.django-rest-framework.org/) and go into school_app/views.py to create our API view.

```bash
    # Install Django Rest Frameworks
    pip install djangorestframework
```
Lets create our view

```python 
# school_app/views.py

# Import APIView and to create our views 
from rest_framework.views import APIView, Response
# and Response to return JSON responses
from django.shortcuts import render
# Import School model
from .models import School

# Create your views here.
class School_Interactions(APIView):
    # Specify the type of request that should trigger this behavior
    def get(self, request):
        # Grab all instances of the School Table and cast it into a list of dictionaries
        all_schools = list(School.objects.all().values())
        # Sort the list of dictionaries by the key of id
        sorted_schools = sorted(all_schools, key=lambda x: x['id'])
        # Return JSON response
        return Response({'schools' : sorted_schools})
```

Now we can move onto our urls and establish a couple of endpoints to start we will go onto our projects urls.py and include our school_app urls.

```python 
from django.contrib import admin
# import include to access different apps urls.py
from django.urls import path, include

# enpoints should be nouns and pluralized
urlpatterns = [
    path('admin/', admin.site.urls),
    # now we can interact with school_app urls
    path('api/v1/schools/', include("school_app.urls")),
]
```

We are telling our project to include school_app/urls.py but currently there is no urls.py file in our school_app. Lets make one and add an empty url enpoint.

```python
# school_app/urls.py

from django.urls import path
# Explicitly import School_Interactions
from .views import School_Interactions

# Remember all urls are prefaced by http://localhost:8000/api/v1/schools/
urlpatterns = [
    # Currently only takes GET requests
    path('', School_Interactions.as_view(), name = 'all_schools'),
]
```


Now that we are done with school_app lets move on to Students and get all students and Exchange Students.

```js
{
    'students': [
        [ 
            {'id': 2, 'name': 'John Avalos', 'email': 'john@gmail.com', 'date_of_birth': datetime.date(2008, 1, 1), 'last_time_at_school': datetime.datetime(2023, 4, 9, 5, 48, 14, 774000, tzinfo=datetime.timezone.utc), 'daily_allowance': Decimal('2.50'), 'year_of_schooling': 15, 'description': 'this is an amazingly bad student', 'good_student': True, 'school_id': 1}, 
            {'id': 3, 'name': 'Jimmy Fallon', 'email': 'jimmy@gmail.com', 'date_of_birth': datetime.date(2008, 1, 1), 'last_time_at_school': datetime.datetime(2023, 4, 9, 6, 12, 32, 480000, tzinfo=datetime.timezone.utc), 'daily_allowance': Decimal('0.00'), 'year_of_schooling': 10, 'description': 'Unkown', 'good_student': True, 'school_id': 1}, 
            {'id': 4, 'name': 'Nick Cage', 'email': 'nick@gmail.com', 'date_of_birth': datetime.date(2008, 1, 1), 'last_time_at_school': datetime.datetime(2023, 4, 10, 5, 47, 58, tzinfo=datetime.timezone.utc), 'daily_allowance': Decimal('0.00'), 'year_of_schooling': 2, 'description': 'Nick Cage is an excellent student that gives his classes everything he can all the time every time.', 'good_student': True, 'school_id': 1}], [
            {'id': 4, 'name': 'Nick Cage', 'email': 'nick@gmail.com', 'date_of_birth': datetime.date(2008, 1, 1), 'last_time_at_school': datetime.datetime(2023, 4, 10, 5, 47, 58, tzinfo=datetime.timezone.utc), 'daily_allowance': Decimal('0.00'), 'year_of_schooling': 2, 'description': 'Nick Cage is an excellent student that gives his classes everything he can all the time every time.', 'good_student': True, 'school_id': 1, 'students_ptr_id': 4}
        ]
    ]
}
```

Lets create our view to grab all students

```python 
# Import APIView and to create our views 
from rest_framework.views import APIView, Response
# and Response to return JSON responses
from django.shortcuts import render
# Import School model
from school_app.models import School
# Import both Students and Exchange_Students
from .models import Students, Exchange_Students
# Create your views here.

class All_Students(APIView):
    
    def get(self, request):
        # Get all students and exchange students as lists of dictionaries
        students = list(Students.objects.all().values())
        exchange_students = list(Exchange_Students.objects.all().values())
        # Sort both students and exchange students by id
        sorted_students = sorted(students, key=lambda x : x['id'])
        sorted_exchange_students = sorted(exchange_students, key=lambda x : x['id'])
        # Create a list of both sorted lists 
        all_students = [sorted_students, sorted_exchange_students]
        # Return a JSON Response of both students and Exchange_Students
        return Response({"students" : all_students})
```

Then add students_app/urls.py to our projects urls

```python
from django.contrib import admin
# import include to access different apps urls.py
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/schools/', include("school_app.urls")),
    # include student_app urls.py file
    path('api/v1/students/', include("students_app.urls")),
]
```

And finally lets link our student_app/urls.py with our view

```python
# students_app/urls.py

from django.urls import path
# Import All_Students
from .views import All_Students

# remember all urls are prefaced by http://localhost:8000/api/v1/students/
urlpatterns = [
    path('', All_Students.as_view(), name = 'all_students')
]
```
