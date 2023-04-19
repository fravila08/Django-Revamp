from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.serializers import serialize
from pokemon_app.models import Pokemon
from move_app.models import Move
from .models import Trainer
import json


# Create your views here.
@method_decorator(login_required, "get")
class Trainer_log(APIView):
    def post(self, request):
        # we can see what user is making the request if any is logged in when the request was made
        # otherwise we will see an AnonymousUser instance
        print(request.user)
        # will return True if a user is making the request and False for AnonymousUser
        if request.user.is_authenticated:
            # in the case it returns true we would know that a logged in user is pinging this endpoint
            # this means the behavior they're looking for is log_out
            logout(request)
            return Response({"log_out": True})
        else:
            # in this case an anonymous user has made the request so lets try to see if we are creating or getting a user
            # by asking django to authenticate the current email and password to a user in our database
            trainer = authenticate(
                username=request.data["email"], password=request.data["password"]
            )
            if trainer is not None and trainer.is_active:
                # if the authentication was successful it means a user in our databse exist with these
                # credentials and is trying to log_in
                login(request, trainer)
                return Response({"log_in": True})
            else:
                # When trainer fails to be authenticated it means there's no trainer existing with this credentials
                # this means the user is trying to sign up for our API
                Trainer.objects.create_user(**request.data)
                return Response({"sign_up": True})

    # what if our user wants to know their current information
    # first we want to ensure whomever is making this get request is a valid and logged in
    # user so we will utilize the login_required decorator which was set by the method decorator
    # at the top of the class
    def get(self, request):
        trainer = Trainer.objects.get(id = request.user.id)
        trainer = json.loads(serialize("json", [trainer], fields=["email", "name", "pokemon"]))
        # we want the user to actually see their pokemon so we have to replace the
        # keys being returned with the Pokemon themselves
        trainer[0]['fields']['pokemon'] = json.loads(serialize('json', request.user.pokemon.all()))
        # again we don't want to just have keys instead we will have to iterate through and 
        # grab each Move instance
        for pokemon in trainer[0]['fields']['pokemon']:
            for move in range(len(pokemon['fields']['moves'])):
                id = pokemon['fields']['moves'][move]
                pokemon['fields']['moves'][move] = json.loads(serialize('json', [Move.objects.get(id = id)]))[0]
        return Response(trainer)
    
 
    

class Master_Sign_Up(APIView):

    def post(self, request):
        master_trainer = Trainer.objects.create_user(**request.data)
        master_trainer.is_staff = True
        master_trainer.is_superuser = True
        master_trainer.save()
        return Response({"sign_up_master": True})

# dispatch means all request to this view will require the user to be logged in
@method_decorator(login_required, 'dispatch')
class Trainer_pokemon(APIView):
    
    def get(self, request):
        # user already holds all pokemon instances we just 
        # need to grab them from request.user
        pokemon= request.user.pokemon.all()
        pokemon = json.loads(serialize('json', pokemon))
        return Response(pokemon)
    
    def put(self, request, pokemon_id):
        # request.user is a set that takes in pokemon Ids/Pks
        request.user.pokemon.add(pokemon_id)
        request.user.save()
        # we don't want to return the number on so we need to grab this 
        # pokemon from the database
        pokemon = Pokemon.objects.get(id = pokemon_id)
        return Response(f"{pokemon.name} has been added to your team")
    
    def delete(self, request, pokemon_id):
        # resquest.user.pokemon is a set of numbers that can utilize remove to 
        # delete an id/pk from the set
        request.user.pokemon.remove(pokemon_id)
        request.user.save()
        # we don't want to return the number on so we need to grab this 
        # pokemon from the database
        pokemon = Pokemon.objects.get(id = pokemon_id)
        return Response(f"{pokemon.name} has been removed from your team")