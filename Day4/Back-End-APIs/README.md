# BACK-END 3rd Party API's

## Topics Covered / Goals

- Using APIs from the backend
  - Many APIs cannot be used easily like we did in week 4 (front end -> api -> front end), for security reasons
  - Send requests from front end -> back end -> api > back end -> front end

## Lesson

> One reason why we might need to use an API from the back end is that many APIs require users to be authenticated to use the API, so you need to send the request from the back end, where you can keep your credentials secret.

    - secret management
        - Never put keys or other secrets in github!
        - use environment variables to supply credentials to your app

> Another reason is because some APIs are inaccessible from the front end, due to the Same Origin Policy (SOP) and lack of Cross Origin Resource Sharing (CORS). This is intended to be a security feature, but it can sometimes be frustrating to work around.

> by default, when you send an AJAX request, browsers only will use responses from servers in the same origin

> example origin, including protocol (https), subdomain, and tld: https://developer.mozilla.org/

> a server that is expecting to receive cross-origin requests can set headers on the response (`access-control-allow-origin: *`), meaning that any client is allowed to use the response

> The process for acquiring and using an API key may be different for different APIs, so be sure to read the documentation. The API Key is a unique key associated with your developer account for billing/usage purposes. You will often have public and/or private API keys - the public key can be used on the front end, since it's not sensitive or private. The private key must be stored securely on the server (using env variables, not in a git repo). If you are getting charged money for using an API, make sure you protect your private key. If anyone gets a hold of your private key, they can impersonate you and you can get charged boatloads of money. Public keys are public - don't worry about protecting these.

> Today, we'll be using the noun project API, but every API is different. [Read the documentation](http://api.thenounproject.com/getting_started.html) in order to know how you're supposed to authenticate and send requests.

> After reading the docs, I want to get an API key. After creating an account, we need to create an 'app', and then we can create a set of keys associated with that app. Before we write any code, we can test our keys in the [api explorer](https://api.thenounproject.com/explorer)

> Now that we have some idea how the API works, let's build a django project that uses it. The first new thing we'll need for this project is a library that will help us send requests, called `requests`. It's similar to axios, except it's used on the back end with python.

```bash
pip install requests
pip install requests_oauthlib
```

```python
import requests
from requests_oauthlib import OAuth1

# public key and private key
auth = OAuth1("*******************", "**********************")
endpoint = "http://api.thenounproject.com/icon/1"

response = requests.get(endpoint, auth=auth)
responseJSON = response.json()
```

> There's a lot of content here! In the browser, it was easier to dig into large data structures, but it's not quite as easy to read large data structures in python due to how they print in the terminal. I'm going to use a built-in python module, pprint (pretty print) that'll help me read the responses from the API.

```python
import pprint

# only go 2 levels deep, so we get a general idea of the response without having to look at the whole thing
pp = pprint.PrettyPrinter(indent=2, depth=2)

response = requests.get(endpoint, auth=auth)
responseJSON = response.json()
pp.pprint(responseJSON)
```

> Now that we can get a response from the API, let's use that data in a template that we send to the client.

> There's one last problem we need to solve before I commit this in github. Currently, my private key is visible in the code, so if I pushed it up to github, other people might steal my credentials. We need to use environment variables, which are not committed in git, to supply credentials to our app. We could use actual env variables in BASH, but it's common practice to use a .env file, which looks a little like this:

```bash
# my .env file
env=prod
apikey=******
secretkey=*****
```

To help us read it, we'll use a python package called `python-dotenv`.

```bash
pip install python-dotenv
```

```python
from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.
print(os.environ['apikey'])

```

> Lets utilize what we just learned and add an app to our pokedex project that could display icons from the Noun Project. In this case let's utilize this to add Pokeballs to our Pokedex project. Create a pokeball_app and do the following:

- Add your secret keys to your .env file (Django Secret Key, Noun Project key, Noun Project Secret Key)

- Install dotenv to load environment keys

- In pokeball_app create a converters.py file and add the following class

```python
# pokeball_app/converters.py
from django.urls import converters

# It's still ensuring it's a string so we don't need regex
class BallTypeConverter(converters.StringConverter):
    # The types of pokeballs we want to be able to accept
    allowed_balls = ['masterball', 'pokeball', 'ultraball', 'greatball']
    # What should Django do when receiving this parameter incorrectly
    def to_python(self, value):
        if value.lower() not in self.allowed_balls:
            raise ValueError('Invalid ball type')
        return value.lower()
```

- In pokeball_app/urls.py add a path that utilizes this converter

```python
#pokeball_app/urls.py
from django.urls import path, register_converter
from .converters import BallTypeConverter
from .views import Pokeball_Img

# register the converter we created so we could utilize it in our paths
register_converter(BallTypeConverter, 'pokeball')

urlpatterns = [
    # utilize the registered converter to ensure the parameter is valid
    path("<pokeball:ball>/", Pokeball_Img.as_view(), name='pokeball'),
]
```

- In pokeball_app/views.py we can now create our View that will send an API call to our 3rd Party API

```python
# pokeball_app/views.py
from rest_framework.views import APIView, Response #<-- Utilize to handle API behavior
from requests_oauthlib import OAuth1 # Authenticates a user with public and secret keys
from dotenv import load_dotenv # Allows us to interact with .env files
import requests # Pythons user friendly way to make requests to API's
import pprint # Will format our JSON data
import os # os will make it possible to grab key value pairs from .env

load_dotenv()
pp = pprint.PrettyPrinter(indent=2, depth=2)

# Create your views here.
class Pokeball_Img(APIView):

    def get(self, request, ball):
        # Grab the url parameter of ball
        auth = OAuth1(os.environ['NOUN_KEY'], os.environ['NOUN_SECRET_KEY'])
        # pass in both the public and secret key from the Noun Project
        endpoint = f"http://api.thenounproject.com/icon/{ball}"
        response = requests.get(endpoint, auth=auth)
        # Send API request to the Noun_project
        responseJSON = response.json()
        pp.pprint(responseJSON['icon']['preview_url'])
        return Response(responseJSON['icon']['preview_url'])
```
- Next connect your pokeball_app/urls.py to the projects/urls.py

```python 
# pokedex_proj/urls.py
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/pokemon/', include('pokemon_app.urls')),
    path('api/v1/moves/', include('move_app.urls')),
    path('api/v1/pokeballs/', include('pokeball_app.urls')),
]
```

- Finally in settings.py import your Django Secret key from your .env and add the pokeball_app onto the registered apps.

```python 
# pokedex_proj/settings.py
SECRET_KEY = os.environ['SECRET_KEY']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pokemon_app',
    'move_app',
    'pokeball_app',
]
```

- Testing works a bit different with API's since we don't want to actually make the API call everytime we run our test. So instead unit tests have the ability to mock API calls. Create a new testing file for this view called test_apis.py

```python
# tests/test_apis.py
import json
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class PokeballImgTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # here we are specifying what specific part of 'requests' we are mocking. In this case we are movking the 
    # get method from our requests meaning a request will never actually be sent
    @patch('requests.get')
    def test_pokeball_img_api_view(self, mock_get):
        ball = 'pokeball'
        preview_url = "https://example.com/image.png"

        # Set up mock return response value for requests.get and assign it to the mock_get method
        mock_response = type('MockResponse', (), {'json': lambda self: {'icon': {'preview_url': preview_url}}})
        mock_get.return_value = mock_response()

        # Make GET request to Pokeball_Img API view
        response = self.client.get(reverse('pokeball', args=[ball]))
        
        # Check that the response status code is 200
        with self.subTest():
            self.assertEqual(response.status_code, 200)

        # Check that the response content is the expected preview URL
        self.assertEquals(json.loads(response.content), preview_url)
```
## Assignments
- [API Show and Tell](https://github.com/tangoplatoon/API-show-and-tell)