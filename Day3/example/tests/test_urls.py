from django.test import TestCase
# We need reverse to be able to ping our own urls by name
# resolve will give us detailed information about our url 
# such as routes, args, views, and more
from django.urls import reverse, resolve
# We will want to have all the views we've created to
# ensure they match with their corresponding url
from pokemon_app.views import All_pokemon, Selected_pokemon
from move_app.views import All_moves, Selected_move


class Test_urls(TestCase):

    def test_001_all_pokemon(self):
        # we will resolve our url to access the information attached to the
        # url instead of seeing it's behavior
        url = resolve(reverse('all_pokemon'))
        # subTest allows us to run more than one assertion within a Test
        with self.subTest():
            # Here we will ensure the url path matches the url route
            self.assertEquals(url.route, 'api/v1/pokemon/')
        # Finally we will assert the correct view is corresponding to this endpoint
        self.assertTrue(url.func.view_class is All_pokemon)

    def test_002_selected_pokemon(self):
        url = resolve(reverse('selected_pokemon', args=['Blastoise']))
        with self.subTest():
            self.assertEquals(url.route, 'api/v1/pokemon/<int_or_str:id>/')
        self.assertTrue(url.func.view_class is Selected_pokemon)

    def test_003_all_moves(self):
        url = resolve(reverse('all_moves'))
        with self.subTest():
            self.assertEquals(url.route, 'api/v1/moves/')
        self.assertTrue(url.func.view_class is All_moves)

    def test_004_selected_move(self):
        url = resolve(reverse('selected_move', args=['Psychic']))
        with self.subTest():
            self.assertEquals(url.route, 'api/v1/moves/<str:name>/')
        self.assertTrue(url.func.view_class is Selected_move)
