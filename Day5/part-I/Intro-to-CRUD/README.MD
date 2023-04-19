# Intro-to-CRUD

## What is CRUD

> CRUD stands for Create, Read, Update, and Delete. It is a commonly used acronym in software development and database management, referring to the four basic functions that are essential for working with persistent data.

> Create refers to the process of adding new data to a system, such as creating a new record in a database or adding a new item to a list.

> Read refers to the process of retrieving existing data from a system, such as querying a database to retrieve a specific record or displaying a list of items.

> Update refers to the process of modifying existing data in a system, such as editing a record in a database or updating the details of an item.

> Delete refers to the process of removing existing data from a system, such as deleting a record from a database or removing an item from a list.

> Together, these four operations provide a foundation for managing data in a wide range of applications and systems.

> So far our application has full READ capabilities but we don't have a way to UPDATE, CREATE, OR DELETE information from our database. In this lesson we will concentrate on the update method and integrate it with our pokedex project by giving users the ability to change a Pokemons level, captured status, and moves. We don't want all of these options to be integrated onto our url itself, instead we will have users send this information through request data and have our views extrapolate this information.

> Inside our views in pokemon_app we already have a `Selected_pokemon` API view that can successfully get a pokemon from our database by either name or id and return it in a Response in JSON format. Now that we want to UPDATE something in the database we will utilize the `PUT` request method to trigger our next set of behavior.

```python
# pokemon_app/views.py
class Selected_pokemon(APIView):
    # lets create a class method to grab a pokemon by id or name
    # to avoid repeating this logic on every single request method.
    def get_pokemon(self, id):
        if type(id) == int:
            return Pokemon.objects.get(id = id)
        else:
            return Pokemon.objects.get(name = id.title())
        
    def get(self, request, id):  # <-- Notice id is now a parameter and its value is being pulled straight from our URL
        pokemon = self.get_pokemon(id)
        json_pokemon = serialize('json', [pokemon])
        serialized_pokemon = json.loads(json_pokemon)
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
```

> Now our users have the ability to ping the same url they use to get a pokemon but instead of sending a `GET` request they will be sending a `PUT` request where the body of the request holds a JSON object resembling the following:

```json
{
    "level_up": 25,
    "captured" : true,
    "moves" : [4, 12, 13, 6]
}
```

> We ourselves will utilize Postman to do this action. We can choose the `PUT` request method to the following url `http://127.0.0.1:8000/api/v1/pokemon/1/` and then add `raw` data to the `body` of the request. Then we can send the request and receive our UPDATED pokemon data.

# Testing PUT views

> Now we have created our view corresponding to the `PUT` method, but we want to be able to test it and ensure everything is working correctly through out the development process.

```python
# tests/test_views.py

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
```

## Extending CRUD

> Now that we have a fully tested put method for pokemon, lets create and test `PUT` method that will allow users to set a new PP value for Pokemon moves. 