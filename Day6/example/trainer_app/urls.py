from django.urls import path
from .views import Trainer_log, Master_Sign_Up, Trainer_pokemon

urlpatterns = [
    path('', Trainer_log.as_view(), name='trainer_log'),
    path('master/', Master_Sign_Up.as_view(), name='master'),
    path('pokemon/', Trainer_pokemon.as_view(), name='all_trainers_pokemon'),
    path('pokemon/<int:pokemon_id>/', Trainer_pokemon.as_view(), name='add_or_sub_a_pokemon'),
]
