# pokemon_app/views.py
from django.shortcuts import render
# We will import the following to read and return JSON data more efficiently
from rest_framework.views import APIView, Response
# We want to bring in our model
from .models import Move
# serialize will turn querysets into binary string
from django.core.serializers import serialize
# Json will turn binary string into JSON readable data
import json

# Create your views here.
class All_moves(APIView):
    # specify which request method should trigger this behavior
    def get(self, request):
        # grab a binary string of all Moves in the DB ordered by name
        moves = serialize('json', Move.objects.all().order_by('name'))
        # utilize json.loads to turn moves into JSON Data
        moves = json.loads(moves)
        return Response(moves)
    
    def post(self, request):
        new_move = Move.objects.create(**request.data)
        new_move.save()
        new_move.full_clean()
        new_move = json.loads(serialize('json', [new_move]))
        return Response(new_move)


class Selected_move(APIView):
    
    def get_a_move(self, name):
        return Move.objects.get(name = name.title())

    def get(self, request, name):
        move = serialize('json', [self.get_a_move(name)])
        move = json.loads(move)
        return Response(move)
    
    def put(self, request, name):
        move = self.get_a_move(name)
        move.pp = request.data['pp']
        move.full_clean()
        move.save()
        move = json.loads(serialize('json', [move]))
        return Response(move)
    
    def delete(self, request, name):
        move = self.get_a_move(name)
        move.delete()
        return Response(f"{name} was deleted")
