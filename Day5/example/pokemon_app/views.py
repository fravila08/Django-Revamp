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
    
    # specify the request method that should trigger this behavior
    def post(self, request):
        # We could create a pokemon by specifying each individual field but that's obviously not optimal
        # new_pokemon = Pokemon.objects.create(name = request.data['name'], level = request.data['level'])
        # instead we can use the kwargs method and pass in request.data (a dict) into the create argument
        new_pokemon = Pokemon.objects.create(**request.data)
        new_pokemon.save()
        new_pokemon.full_clean()
        new_pokemon = json.loads(serialize('json', [new_pokemon]))
        return Response(new_pokemon)



class Selected_pokemon(APIView):
    # lets create a class method to grab a pokemon by id or name
    # to avoid repeating this logic on every single request method.
    def get_pokemon(self, id):
        if type(id) == int:
            return Pokemon.objects.get(id = id)
        else:
            return Pokemon.objects.get(name = id.title())
        
    #  Specify the method to trigger this behavior
    def get(self, request, id):  # <-- Notice id is now a parameter and its value is being pulled straight from our URL
        # Lets initialize pokemon as None and give it a
        # corresponding query set depending on the ids type
        pokemon = self.get_pokemon(id)
        # Since pokemon is a single instance it needs to be wrapped by [] to make it
        # iterable for the serialize function to turn it into a binary string
        json_pokemon = serialize('json', [pokemon])
        serialized_pokemon = json.loads(json_pokemon)
        # return Response(unserialized_pokemon)
        return Response(serialized_pokemon)

    def put(self, request, id):  # <-- ID is our url parameter
        # we still want to grab a pokemon either by ID or by name
        pokemon = self.get_pokemon(id)
        # Now we have to check the body of our request and check if
        # the following keys are in our request ['level_up', 'captured', 'moves']
        if 'level_up' in request.data:
            # we will level up a pokemon to the desired level
            pokemon.level_up(request.data['level_up'])
        if 'captured' in request.data:
            # a pokemons captured status will be set to this value
            pokemon.change_caught_status(request.data['captured'])
        if 'moves' in request.data:
            # pokemons moves will be set to the following integer list
            pokemon.moves.set(set(request.data['moves']))
        # full clean to check our validations
        pokemon.full_clean()
        # save all changes
        pokemon.save()
        # serialize our updated pokemon and return it as json
        pokemon = json.loads(serialize('json', [pokemon]))
        return Response(pokemon)
        
    def delete(self, request, id):
        # get a pokemon from our database
        pokemon = self.get_pokemon(id)
        # grab the pokemons name before deleting to utilize in the Response message
        pokemon_name = pokemon.name
        # delete instance and database entry
        pokemon.delete()
        # return the name of the pokemon deleted
        return Response(f"{pokemon_name} was deleted")