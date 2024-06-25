from django.test import TestCase

from .scraping import get_google_places_data
from .creds import gmaps_api_key

# Create your tests here.

class PlaceholderTest(TestCase):
    def test_get_google_data(self):
        result = get_google_places_data(gmaps_api_key, "Coles", "Subiaco")["places"][0]["id"]
        expected = "ChIJMTdRtBalMioRXVl7CoFy9yM"
        self.assertEqual(result, expected)