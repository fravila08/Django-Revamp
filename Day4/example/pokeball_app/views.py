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
        # pp.pprint(responseJSON['icon']['preview_url'])
        return Response(responseJSON['icon']['preview_url'])
