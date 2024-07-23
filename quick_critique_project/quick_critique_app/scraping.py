import requests
import json
import serpapi
from django.utils import timezone
from datetime import timedelta
from .creds import gmaps_api_key, serp_api_key
from .models import Restaurant, ReviewSummary
from .analysis import summarise_reviews

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
    response = requests.post(url, headers=headers, data=json.dumps(data), timeout=60)
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

def generate_review_data(restaurant_name: str, city_name: str):
    # Get place_id from Google Places API
    places_data = get_google_places_data(restaurant_name, city_name)
    place_details, place_id = extract_place_details(places_data)
    print("Place ID:", place_id, "identified.")
    
    if place_id:
        # Check if the restaurant is already in the database by place_id
        try:
            restaurant = Restaurant.objects.get(place_id=place_id)
            # Check if the summary is up-to-date (e.g., within the last 28 days)
            if ReviewSummary.objects.filter(restaurant=restaurant, last_updated__gte=timezone.now() - timedelta(days=28)).exists():
                review_summary = ReviewSummary.objects.get(restaurant=restaurant)
                print("Located in database. Serving from cache.")
                place_details = {
                    'displayName': restaurant.display_name,
                    'rating': restaurant.rating,
                    'userRatingCount': restaurant.user_rating_count
                }
            else:
                # If the summary is out of date, behave the same was as if the restaurant has not been reviewed
                raise Restaurant.DoesNotExist

        except Restaurant.DoesNotExist:
            # If not in the database, fetch the details and save them
            print("Not found in database, pulling fresh reviews.")
            reviews = get_reviews(place_id)
            restaurant, created = Restaurant.objects.get_or_create(
                place_id=place_id,
                defaults={
                    'name': restaurant_name,
                    'city': city_name,
                    'display_name': place_details.get('displayName', f"{restaurant_name} in {city_name}"),
                    'rating': place_details.get('rating'),
                    'user_rating_count': place_details.get('userRatingCount')
                }
            )
            # Build the object
            review_summary_text = summarise_reviews(reviews)
            review_summary = ReviewSummary.objects.create(
                restaurant=restaurant,
                food=review_summary_text.get('Food', ''),
                service=review_summary_text.get('Service', ''),
                atmosphere=review_summary_text.get('Atmosphere', ''),
                price=review_summary_text.get('Price', ''),
                trend=review_summary_text.get('Trend', ''),
                summary=review_summary_text.get('Summary', '')
            )
    else:
        # Handle case where place_id could not be retrieved
        pass

    return restaurant, place_details, review_summary