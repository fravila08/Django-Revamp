# Expanding endpoints and implementing Tests

## Lesson

By the end of this lesson we will have a better undersnding of flexible endpoints and how to implement tests to both urls and views.

## Expanding Endpoints

Lets Expand on our current enpoints and crate the ability to grab a single specific instance from our database.


Now in order for a user to request a specific pokemon instance, we need to give our user a way to give us that specific information either through the body of our URL or through the URL itself. Django has a couple of built in parameter we can add to our URL's but for the purpose of this course we will focus on `str`, `int`, and `custom` URL parameters. 

- str and int parameters

```python
    # In this case we are telling Django that after '...pokemon/' we will recieve an '...pokemon/interger/' and it will be ended by a slash
    int_path = 'http://127.0.0.1:8000/api/v1/pokemon/<int:id>/' # 1, 22, 176 (ACCEPTABLE) | Blastoise, Pikachu (UNACCEPTABLE)

    str_path = 'http://127.0.0.1:8000/api/v1/pokemon/<str:id>/' # 1, 22, 176 (UNACCEPTABLE) | Blastoise, Pikachu (ACCEPTABLE)
```

Now what if I need my API to be flexible and be able to take in both int and string? Well Django doesn't provide me with that option. I could stablish both paths and Django will default to which ever path works but that leaves a lot of chance up to Django and it's better for us to have control of our program. So lets create a custom "type" for our parameter that will take in both str or an int type.


Create a converters.py file in pokemon_app and create the following class.

```python
# pokemon_app/converters.py

class IntOrStrConverter:
    # The regex attribute is a regular expression that matches any sequence of digits or alphabetic characters. 
    # It is used by Django to match URL patterns against incoming URLs.
    regex = '[0-9]+|[a-zA-Z]+'
    # The to_python method is called by Django when it matches a URL pattern that uses 
    # this converter. It takes the matched string as input and returns the converted value. 
    def to_python(self, value):
        if value.isdigit():
            return int(value)
        else:
            return str(value)
    # The to_url method is called by Django when it generates URLs that use this converter. It takes 
    # the converted value as input and returns a string that can be used in a URL.
    def to_url(self, value):
        return str(value)

```

Now we can import this class into pokemon_app/urls.py and register it as a converter for url parameters as such

```python
#pokemon_app/urls.py
# import register converter to create new param types in URL patterns
from django.urls import path, register_converter
# Explicit imports
from .views import All_pokemon, Selected_pokemon
# import our converter class to utilize as a parameter type
from .converters import IntOrStrConverter

# To use this custom converter in a URL pattern, you need to register it with Django using the register_converter function.
register_converter(IntOrStrConverter, 'int_or_str')
# Remember all urls are prefaced by http://localhost:8000/api/v1/pokemon/
urlpatterns = [
    # Currently only takes GET requests
    path('', All_pokemon.as_view(), name='all_pokemon'),
    # now we can utilize our converter for the variable we provided
    path('<int_or_str:id>/', Selected_pokemon.as_view(), name='selected_pokemon')
]
```

We have a url pattern established and created a `type` for a url parameter... but how does that connect to our views? In pokemon_app/views lets create a `Selected_pokemon` view that will take in a get request and the id of the pokemon the user is looking for and then returns an individual pokemon instance.


```python
# pokemon_app/views

class Selected_pokemon(APIView):
    #  Specify the method to trigger this behavior
    def get(self, request, id):  # <-- Notice id is now a parameter and its value is being pulled straight from our URL
        # Lets initialize pokemon as None and give it a
        # corresponding query set depending on the ids type
        pokemon = None
        # id is an int
        if type(id) == int:
            pokemon = Pokemon.objects.get(id=id)
        # id is a string
        else:
            pokemon = Pokemon.objects.get(name=id.title())
        # Since pokemon is a single instance it needs to be wrapped by [] to make it 
        # iterable for the serialize function to turn it into a binary string
        json_pokemon = serialize('json', [pokemon])
        serialized_pokemon = json.loads(json_pokemon)
        # return Response(unserialized_pokemon)
        return Response(serialized_pokemon)
```

Users can now get a single pokemon instance by either pokemons name or pokemons ID! Now lets create a url path and view for grabbing a single pokemon move by name.

```python
# move_app/urls.py
from django.urls import path
from .views import All_moves, Selected_move

urlpatterns = [
    path('', All_moves.as_view(), name='all_views'),
    path('<str:name>/', Selected_move.as_view(), name='selected_move' )
]
```

Now we can create the Selected_move class and take in the name parameter

```python
# move_app/views.py
class Selected_move(APIView):

    def get(self, request, name):
        move = serialize('json', [Move.objects.get(name = name.title())])
        move = json.loads(move)
        return Response(move)
```

## Testing our API enpoints

Now that we have some extensive data and relationships created, we will want to utilize fixtures in our tests to mimick our current data available from our Database. Create some fixtures using `dumpdata` onto each app. 


As we can see our App's are becoming more and more complex as their relationships grow. In order to test them both correctly we will have to do a bit of folder restructure. So let's get started

- On the same level as your apps and project create a new directory called `tests`

- Inside of tests create a file `test_models.py` and move all of our pre-existing tests onto this file. Once you've done that you could delete the tests.py file in each app.

- Inside the tests directory create a test_views.py and an answers.py

- Fill in answers.py with the results we receive from pinging our API this way we can import the information onto our test files to ensure it stays consistent.

- In test_views.py we can create tests to ensure our views are producing the desired behavior.

```python
# tests/test_views.py

# A client must ping our api in order for our views to be triggered.
from django.test import TestCase, Client
# We can't make calls ourselves to this api so we will utilize reverse to mock this behavior
from django.urls import reverse
# we can import all the expected answers from our answer.py file
from tests.answers import all_pokemon, a_pokemon, all_moves, a_move
import json


class Test_views(TestCase):
    # We dont have a database so we will mock our DB through fixtures
    fixtures = [
        "pokemon_data.json",
        "move_data.json"
    ]
    # We will need a client for every test, instead of re-writing  this 
    # instance we can use the set up method to access the client on every
    # test by prepending it with self
    def setUp(self):
        client = Client()

    def test_001_get_all_pokemon(self):
        # client sends a get request to a url path by url name
        response = self.client.get(reverse('all_pokemon'))
        response_body =json.loads(response.content)
        # we want our responses body to be equal to our answer from answer.py
        self.assertEquals(response_body, all_pokemon)

    def test_002_get_a_pokemon(self):
        # client sends a get request to a url path by url name. 
        response = self.client.get(reverse('selected_pokemon', args=['pikachu']))
        # since our URL has an integrated parameter, we can pass it's value through args
        response_body = json.loads(response.content)
        self.assertEquals(response_body, a_pokemon)
    # REPEAT THE PROCESS FOR THE MOVE_APP
```

- Create a test_urls.py where we can ensure the correct path and view is attached to each url.

```python
# tests/test_urls.py
from django.test import TestCase
# We need reverse to be able to ping our own urls by name
# resolve will give us detailed information about our url 
# such as routes, args, views, and more
from django.urls import reverse, resolve
# We will want to have all the views we've created to
# ensure they match with their corresponding url
from pokemon_app.views import All_pokemon, Selected_pokemon
from move_app.views import All_moves, Selected_move


class Test_urls(TestCase):

    def test_001_all_pokemon(self):
        # we will resolve our url to access the information attached to the
        # url instead of seeing it's behavior
        url = resolve(reverse('all_pokemon'))
        # subTest allows us to run more than one assertion within a Test
        with self.subTest():
            # Here we will ensure the url path matches the url route
            self.assertEquals(url.route, 'api/v1/pokemon/')
        # Finally we will assert the correct view is corresponding to this endpoint
        self.assertTrue(url.func.view_class is All_pokemon)

# DO THE SAME FOR REMAINDING ENDPOINTS
```

- Now we can run the test suite and watch all 12 of our existing test pass or fail. Currently we know our API is working the way we want it too up to this point, so if a test fails adjust it to fit your behavior. Once adjusted, tests shouldn't be touched again since they are our easiest way of ensuring our application is continuously working as desired.

```bash
    python manage.py test tests
```
