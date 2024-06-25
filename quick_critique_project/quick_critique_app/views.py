from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .forms import ReviewForm
from .scraping import get_google_places_data, extract_place_details, get_reviews
from .analysis import summarise_reviews
from .models import Restaurant, ReviewSummary

def index(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            restaurant_name = form.cleaned_data['restaurant_name']
            city_name = form.cleaned_data['city_name']

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
                        return render(request, 'quick_critique_app/result.html', {
                            'title': restaurant.display_name,
                            'place_details': place_details,
                            'review_summary': {
                                'Food': review_summary.food,
                                'Service': review_summary.service,
                                'Atmosphere': review_summary.atmosphere,
                                'Price': review_summary.price,
                                'Trend': review_summary.trend,
                                'Summary': review_summary.summary
                            },
                            'summary_date': review_summary.last_updated.strftime("%d/%m/%Y.")
                        })
                except Restaurant.DoesNotExist:
                    # If not in the database, fetch the details and save them
                    pass

                # Fetch reviews if not found in database
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
                return render(request, 'quick_critique_app/result.html', {
                    'title': place_details.get('displayName', f"{restaurant_name} in {city_name}"),
                    'place_details': place_details,
                    'review_summary': {
                        'Food': review_summary.food,
                        'Service': review_summary.service,
                        'Atmosphere': review_summary.atmosphere,
                        'Price': review_summary.price,
                        'Trend': review_summary.trend,
                        'Summary': review_summary.summary
                    },
                    'summary_date': "Today"
                })
            else:
                # Handle case where place_id could not be retrieved
                pass

    else:
        form = ReviewForm()
    return render(request, 'quick_critique_app/index.html', {'form': form})
