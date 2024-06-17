import requests
import json
import serpapi
from .creds import gmaps_api_key, serp_api_key

def get_google_places_data(gmaps_api_key, restaurant_name, city_name):
    url = 'https://places.googleapis.com/v1/places:searchText'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': gmaps_api_key,
        'X-Goog-FieldMask': 'places.displayName,places.rating,places.userRatingCount,places.id'
    }
    data = {
        'textQuery': f'{restaurant_name} in {city_name}'
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def extract_place_details(response_data):
    if 'places' in response_data and response_data['places']:
        # Assuming we only need the first result, this might need to be tested
        place = response_data['places'][0]
        place_details = {
            'displayName': place.get('displayName', {}).get('text', ''),
            'rating': place.get('rating', ''),
            'userRatingCount': place.get('userRatingCount', ''),
        }
        place_id = response_data['places'][0]['id']
        print(place_details)
        print(place_id)
        return place_details, place_id
    return None, None

def get_reviews(restaurant_name, city_name):
    
    places_data = get_google_places_data(gmaps_api_key, restaurant_name, city_name)
    place_details, place_id = extract_place_details(places_data)

    if not place_id:
        return [], None
    
    params = {
    "api_key": serp_api_key,
    "engine": "google_maps_reviews",
    "hl": "en",
    "place_id": place_id,
    "sort_by": "newestFirst"
    }

    search1 = serpapi.search(params)
    results1 = search1.as_dict()
    reviews = results1["reviews"]
    
    # Handle pagination if necessary
    #if "next_page_token" in results1.get("serpapi_pagination", {}):
        #params["next_page_token"] = results1["serpapi_pagination"]["next_page_token"]
        #search2 = serpapi.search(params)
        #results2 = search2.as_dict()
        #reviews += results2["reviews"]

    # add some code here to loop this a few times to get more reviews
    print(reviews)
    return place_details, reviews