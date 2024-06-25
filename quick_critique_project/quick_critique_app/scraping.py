import requests
import json
import serpapi
from .creds import gmaps_api_key, serp_api_key

def get_google_places_data(restaurant_name, city_name):
    url = 'https://places.googleapis.com/v1/places:searchText'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': gmaps_api_key,
        'X-Goog-FieldMask': 'places.displayName,places.rating,places.userRatingCount,places.id'
    }
    data = {
        'textQuery': f'{restaurant_name} in {city_name}'
    }
    print("Searching Google for the place_id.")
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
        return place_details, place_id
    return None, None

def extract_relevant_fields(reviews):
    concise_reviews = []

    for review in reviews:
        review_info = {
            'rating': review.get('rating'),
            'iso_date': review.get('iso_date'),
            'local_guide': review['user'].get('local_guide', False),
            'reviews': review['user'].get('reviews', 0),
            'snippet': review.get('snippet'),
            'details': review.get('details')
        }
        concise_reviews.append(review_info)

    return concise_reviews

def get_reviews(place_id):
    params = {
        "api_key": serp_api_key,
        "engine": "google_maps_reviews",
        "hl": "en",
        "place_id": place_id,
        "sort_by": "newestFirst"
    }

    reviews = []
    # Loop through the first 5 pages
    for _ in range(4):  
        search = serpapi.search(params)
        results = search.as_dict()
        reviews.extend(results.get("reviews", []))
        # Check for next page token
        pagination = results.get("serpapi_pagination", {})
        next_page_token = pagination.get("next_page_token")
        if next_page_token:
            params["next_page_token"] = next_page_token
        else:
            # No more pages, break out of the loop
            break  
    concise_reviews = extract_relevant_fields(reviews)
    return concise_reviews
