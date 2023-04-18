from django.shortcuts import render
# We will import the following to read and return JSON data more efficiently
from rest_framework.views import APIView, Response
from rest_framework.parsers import JSONParser
# We want to bring in our model
from .models import Pokemon
# We will utilize serializer to turn our QuerySets into
# binary string
from django.core.serializers import serialize
# Json.loads will turn binary strings into JSON data
import json

# Create your views here.


class All_pokemon(APIView):
    # Establish the method that will trigger this behavior
    def get(self, request):
        # Grab all Pokemon existing within our database in a
        # specific order to keep consistency. In this case
        # we will order our data by name in aphabetical order
        pokemon = Pokemon.objects.all().order_by('name')
        # we can't send back query sets as a valid JSON response
        # so we will utilize Django's built in serialize function
        # to turn our query set into a binary string
        serialized_pokemon = serialize('json', pokemon)
        # Now we can use the python json.loads function to turn
        # our binary string into a workable json format
        json_pokemon = json.loads(serialized_pokemon)
        return Response(json_pokemon)


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
