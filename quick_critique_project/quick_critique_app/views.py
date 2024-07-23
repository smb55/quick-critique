from django.shortcuts import render
from .forms import ReviewForm
from .scraping import generate_review_data

def index(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            restaurant_name = form.cleaned_data['restaurant_name']
            city_name = form.cleaned_data['city_name']
            
            restaurant, place_details, review_summary = generate_review_data(restaurant_name, city_name)

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

    else:
        form = ReviewForm()
    return render(request, 'quick_critique_app/index.html', {'form': form})
