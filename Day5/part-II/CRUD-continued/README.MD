# CRUD: Create & Delete

> So far our application has `READ` and `UPDATE` capabilities for both Moves and Pokemon. Lets go into the last two methods that we will need to have in order to have a full CRUD API.

| METHOD    | BEHAVIOR |
| :-------- | :------- |  
| GET       | READ     | 
| PUT       | UPDATE   | 
| POST      | CREATE   | 
| DELETE    | DELETE   |

## Create

> When we create something we are technically POSTING something new onto our database. With that said any type of CREATE behaviour should correlate with the POST request method. Lets go onto pokemon_app/views.py and add this post behavior to our All_pokemon class.

```python
# pokemon_app/views.py

class All_pokemon(APIview):
 # specify the request method that should trigger this behavior
    def post(self, request):
        # We could create a pokemon by specifying each individual field but that's obviously not optimal
        new_pokemon = Pokemon.objects.create(name = request.data['name'], level = request.data['level'])
        # instead we can use the kwargs method and pass in request.data (a dict) into the create argument
        new_pokemon = Pokemon.objects.create(**request.data)
        new_pokemon.save()
        new_pokemon.full_clean()
        new_pokemon = json.loads(serialize('json', [new_pokemon]))
        return Response(new_pokemon)
```
> Now that we have a flexible and well constructed API view to create a Pokemon, we can test it with Postman by sending a POST request to `http://127.0.0.1:8000/api/v1/pokemon/` with all of the new pokemons values inside of the requests data. 

```json
// This is what the data object should look like
{
    "name":"Geodude", //Name does not have a default value, ensure to pass it in the request
    "level": 22,
    "description": "Geodude is a rock type pokemon that will eventually evolve into graveler",
    "captured": true
}
```

> Our API is working correctly, so lets create a test for this function to ensure it continues working correctly through out the development process.

```python
# tests/test_views.py

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
```

## Delete

> Deleting an item from a database is surprisingly simple. We could utilize the already established `Selected_pokemon` view to get a pokemon instance and then call the .delete() mehtod to delete an item from our database.

```python
# pokemon_app/views.py

def delete(self, request, id):
        # get a pokemon from our database
        pokemon = self.get_pokemon(id)
        # grab the pokemons name before deleting to utilize in the Response message
        pokemon_name = pokemon.name
        # delete instance and database entry
        pokemon.delete()
        # return the name of the pokemon deleted
        return Response(f"{pokemon_name} was deleted")
```
> Now we can test it by sending a DELETE request to `http://127.0.0.1:8000/api/v1/pokemon/geodude/` and our API should return a response of "Geodude was deleted"

> Now we need to create a test to ensure this behavior continues to work properly through out the development process.

```python
# tests/test_views.py
def test_008_deleting_a_pokemon(self):
    # after every test the Database resets back to only having fixture data
    # we can call test_007 where the test creates Geodude and then 
    # delete it
    self.test_007_create_a_pokemon()
    response = self.client.delete(reverse('selected_pokemon', args=['geodude']))
    response = json.loads(response.content)
    self.assertEquals(response, "Geodude was deleted")
```
> Perfect, we now have a fully CRUD capable pokemon_app lets take what we've learned and apply it to move_app in order to have a CRUD capabilities around our whole API