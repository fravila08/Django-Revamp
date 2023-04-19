# Django Auth

## Topics Covered / Goals

- The user model
- sign up, log in, log out
- accessing the user from the request object

## Lesson

> Today we will learn how to add Users to our API's and how to create relationships between our users and pokemon.

### The User Model

> We will create a subclass of django's built-in `AbstractUser` class. This is a full, functional user model, that we can also extend with custom properties. We'll use this option today to get a balance between convenience and flexibility.

> Let's go ahead and create a trainer_app to track all of our users/trainers that have accounts on our API. Don't forget to add the app under installed_apps in the projects settings.py

```bash
    python manage.py startapp trainer_app
```

  ```python
  from django.db import models
  from django.contrib.auth.models import AbstractUser

  # Inheriting from 'AbstractUser' lets us use all the fields of the default User,
  # and overwrite the fields we need to change
  # This is different from 'AbstractBaseUser', which only gets the password management features from the default User,
  # and needs the developer to define other relevant fields.
  class Trainer(AbstractUser):
      email = models.EmailField(
          verbose_name='email address',
          max_length=255,
          unique=True,
      )
      # notice the absence of a "Password field", that is built in.

      # django uses the 'username' to identify users by default, but many modern applications use 'email' instead
      USERNAME_FIELD = 'email'
      REQUIRED_FIELDS = [] # Email & Password are required by default.
  ```

> Since we're not using the default, built-in User model, we have to tell django which model we're using for our users in the settings.py file.

```python
# pokedex_proj/settings.py
AUTH_USER_MODEL = 'trainer_app.Trainer'
```
> Finally we can `makemigrations` and `migrate` our model into our database

### Sign up, Log in, Log out

> Now that we've defined our user model by extending `AbstractUser`, we can define views that leverage django's built-in authentication functionality. First, let's define a URL for the views we'll create.

```python
from django.urls import path
from .views import Trainer_log

urlpatterns = [
    path('', Trainer_log.as_view(), name='trainer_log')
]
```

> Now lets start creating our API view, note we aren't doing any CRUD activity here so our entire user functionalities will fall under the POST and GET method only. 

```python
# trainer_app/views.py
from rest_framework.views import APIView, Response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.serializers import serialize
from .models import Trainer
import json


# Create your views here.
@method_decorator(login_required, 'get')
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
            return Response({"log_out":True})
        else:
            # in this case an anonymous user has made the request so lets try to see if we are creating or getting a user
            # by asking django to authenticate the current email and password to a user in our database
            trainer = authenticate(username=request.data['email'], password=request.data['password'])
            if trainer is not None and trainer.is_active:
                # if the authentication was successful it means a user in our databse exist with these
                # credentials and is trying to log_in
                login(request, trainer)
                return Response({"log_in":True})
            else:
                # When trainer fails to be authenticated it means there's no trainer existing with this credentials
                # this means the user is trying to sign up for our API
                Trainer.objects.create_user(**request.data)
                return Response({"sign_up":True})

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
```

> Django handles all the password hashing in one line of code, which is very convenient. If we want to see what django just created for us, let's look in the database.
> Notice that their plain-text password is not included in their record. The password field contains their password hash, which also contains the hashing algorithm and the salt, separated by `$`. Some of the other fields are empty, because they exist by default, but we never set them. Some of the fields will be automatically set by django, however. The fields `date_joined` and `last_login` are updated automatically, like you'd expect. The field `is_active` defaults to True. If you need to delete a user, you should set this to False instead of actually deleting the user. Modern applications rarely permanently delete data, but instead mark items as 'deleted' so that they can be ignored by other queries. Especially for users, it's important to never delete their database record, in case they want to reactivate their account, or if they had connections to other users.

## Handling Super Users
> Now that we've created an `AbstractUser` you'll notice you can't log into the Django Admin page to manage your database. This is because Django's default superuser is no longer active for this project. Now we will have to manually handle this by creating a seperate view that will specifically trigger the creation of admin users.


> Let's create a view and url path to create a Master_Trainer

```python
    path('master/', Master_Sign_Up.as_view(), name='master')

    class Master_Sign_Up(APIView):

        def post(self, request):
            master_trainer = Trainer.objects.create_user(**request.data)
            master_trainer.is_staff = True
            master_trainer.is_superuser = True
            master_trainer.save()
            return Response({"sign_up_master": True})
```
> Finally we could create a master_trainer through postman, register the Trainer model onto the admin site, and log into Django Admin.

## Relationships

> Now we have the ability to have users, so maybe we would like users to be able to capture pokemon. Lets add the following fields to our Trainer model.

```python
    name = models.CharField(max_length=250, default='Unknown')
    pokemon = models.ManyToManyField(Pokemon)
```

> We've added these two fields so lets reflect them in the GET method for the Trainer_log class.

```python

def get(self, request):
    # Notice we've added both name and pokemon to the fields list
    trainer = json.loads(serialize("json", [request.user], fields=["email", "name", "pokemon"]))
    return Response(trainer)
```

> Finally let's create a class and url path allowing us to get our pokemon relationships, and put or delete pokemon to and from our pokemon relationship.

```python
#url paths
    # GET 
    path('pokemon/', Trainer_pokemon.as_view(), name='all_trainers_pokemon'),
    # PUT and DELETE
    path('pokemon/<int:pokemon_id>/', Trainer_pokemon.as_view(), name='add_or_sub_a_pokemon'),

# view
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
```



## External Resources

- [django auth docs](https://docs.djangoproject.com/en/4.0/topics/auth/default/)

