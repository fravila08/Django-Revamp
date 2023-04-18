import json
from unittest.mock import patch
from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse


class PokeballImgTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    # here we are specifying what specific part of 'requests' we are mocking. In this case we are movking the 
    # get method from our requests meaning a request will never actually be sent
    @patch('requests.get')
    def test_pokeball_img_api_view(self, mock_get):
        ball = 'pokeball'
        preview_url = "https://example.com/image.png"

        # Set up mock return response value for requests.get and assign it to the mock_get method
        mock_response = type('MockResponse', (), {'json': lambda self: {'icon': {'preview_url': preview_url}}})
        mock_get.return_value = mock_response()

        # Make GET request to Pokeball_Img API view
        response = self.client.get(reverse('pokeball', args=[ball]))
        
        # Check that the response status code is 200
        with self.subTest():
            self.assertEqual(response.status_code, 200)

        # Check that the response content is the expected preview URL
        self.assertEquals(json.loads(response.content), preview_url)
