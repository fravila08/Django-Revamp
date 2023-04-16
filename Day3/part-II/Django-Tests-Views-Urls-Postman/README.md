# Testing Views, Urls and Utilizing Postman

Now that we have everything connected lets create a test for this url and correlating views return value.

```python
# We need to import Client to send client requests through our Test Suite
from django.test import TestCase, Client
# Since we are currently in our backend we will utilize the reverse method to send
# requests to our urls
from django.urls import reverse
from ..models import School



class school_views_test(TestCase):
    # We don't have a DB so we will use fixtured to preload data onto our
    # test DB by passing the 'fixtures' argument
    fixtures=['school_data.json']
    # We need to use the Client through various test so lets create a setUp
    # to access our client through all of our tests
    def setUp(self):
        client = Client()


    def test_001_School_Interactions_GET(self):
            # answer will represent  our expected output
            answer = {'schools': [{'id': 1, 'name': 'Code Platoon'}, {'id': 2, 'name': 'Code Academy'}]}
            # reverse will utilize the url paths name as an argument to link with 
            # individual urls
            url = reverse('all_schools')
            # we will utilize the client to send a get request to the specified url
            response = self.client.get(url)
            with self.subTest():
                # With subTest we will ensure our status code returns as a 200
                self.assertEquals(response.status_code, 200)
            # we want to ensure the data returned is equal to the answer
            self.assertEquals(response.data, answer)
```

