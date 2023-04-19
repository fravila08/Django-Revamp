from django.db import models
from django.contrib.auth.models import AbstractUser
from pokemon_app.models import Pokemon

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
    name = models.CharField(max_length=250, default='Unknown')
    pokemon = models.ManyToManyField(Pokemon, related_name='pokemon')

    def __str__(self):
        return self.email
    
    
    