# A client must ping our api in order for our views to be triggered.
from django.test import TestCase, Client
# We can't make calls ourselves to this api so we will utilize reverse to mock this behavior
from django.urls import reverse
# we can import all the expected answers from our answer.py file
from tests.answers import all_pokemon, a_pokemon, all_moves, a_move, updated_pokemon, updated_move, new_move
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

    def test_003_get_all_moves(self):
        response = self.client.get(reverse('all_moves'))
        response_body = json.loads(response.content)
        self.assertEquals(response_body, all_moves)

    def test_004_get_a_move(self):
        response = self.client.get(reverse('selected_move', args=['psychic']))
        response_body = json.loads(response.content)
        self.assertEquals(response_body, a_move)

    # ensure names are specific to what's going on in the test
    def test_005_update_pokemon_data(self):
        # Theres a couple of differences in the way we send this request through our client.
        # 1. Notice that our client is specifically sending a PUT request to our URL
        # 2. We are no passing a data parameter holding a dictionary that will be passed to the request
        # 3. By default Django send "application/octet-stream" data in tests so we have to specify that
        #    we are sending "application/json" data in content_type
        response = self.client.put(reverse('selected_pokemon', args=['pikachu']), data={
            "level_up": 25,
            "captured" : True,
            "moves" : [4, 12, 13, 6]
        }, content_type="application/json")
        # This turns the body of our response onto a JSON object
        response_body = json.loads(response.content)
        # updated_pokemon would be the same information we received from Postman
        self.assertEquals(response_body, updated_pokemon)

    def test_006_update_move_pp(self):
        response = self.client.put(reverse('selected_move', args=['Blizzard']), data={
            'pp':7
        }, content_type="application/json")
        response_body = json.loads(response.content)
        self.assertEquals(response_body, updated_move)

    def test_007_create_a_pokemon(self):
        # First lets send a post request with the corresponding data
        response = self.client.post(reverse('all_pokemon'), data={
            "name":"Geodude",
            "level": 22,
            "description": "Geodude is a rock type pokemon that will eventually evolve into graveler",
            "captured": True
        }, content_type="application/json")
        with self.subTest():
            # The date encountered is default to .now() so 
            # we can't create an answer for this code instead
            # we can ensure the request was successful
            self.assertEquals(response.status_code, 200)
        # We know the request was successful so now lets grab the pokemon
        # we created and ensure it exists within the database
        pokemon = self.client.get(reverse('selected_pokemon', args=['geodude']))
        pokemon = json.loads(pokemon.content)
        self.assertIsNotNone(pokemon)

    def test_008_deleting_a_pokemon(self):
        # after every test the Database resets back to only having fixture data
        # we can call test_007 where the test creates Geodude and then 
        # delete it
        self.test_007_create_a_pokemon()
        response = self.client.delete(reverse('selected_pokemon', args=['geodude']))
        response = json.loads(response.content)
        self.assertEquals(response, "Geodude was deleted")

    def test_009_create_a_move(self):
        response = self.client.post(reverse('all_moves'), data={
            "name":"Solar Beam"
        }, content_type="application/json")
        move = json.loads(response.content)
        self.assertEquals(move, new_move)

    def test_010_delete_a_move(self):
        self.client.post(reverse('all_moves'), data={
            "name":"Solar Beam"
        }, content_type="application/json")
        response = self.client.delete(reverse('selected_move', args=['Solar Beam']))
        response = json.loads(response.content)
        self.assertEquals(response, "Solar Beam was deleted")