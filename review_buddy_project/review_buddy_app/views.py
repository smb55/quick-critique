from django.shortcuts import render
from .forms import ReviewForm
from .scraping import get_reviews

def index(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            restaurant_name = form.cleaned_data['restaurant_name']
            city_name = form.cleaned_data['city_name']

            

            # Get place details and reviews
            place_details, reviews = get_reviews(restaurant_name, city_name)
            summary = f"Summary for {restaurant_name} in {city_name}"
            
            return render(request, 'review_buddy_app/result.html', {
                'summary': summary,
                'place_details': place_details,
                'reviews': reviews
            })

            # Placeholder for AI processing logic

    else:
        form = ReviewForm()
    return render(request, 'review_buddy_app/index.html', {'form': form})
