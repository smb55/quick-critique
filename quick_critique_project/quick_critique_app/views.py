from django.shortcuts import render
from .forms import ReviewForm, BulkReviewForm
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

def bulk_reviews(request):
    if request.method == 'POST':
        form = BulkReviewForm(request.POST, request.FILES)
        if form.is_valid():
            bulk_file = request.FILES['bulk_file']
            city_name = bulk_file.readline().strip().decode('utf-8')
            restaurant_names = [line.strip().decode('utf-8') for line in bulk_file.readlines()]

            results = []
            for restaurant_name in restaurant_names:
                try:
                    print("Processing:", restaurant_name)
                    generate_review_data(restaurant_name, city_name)
                    results.append(f"{restaurant_name} processed successfully.")
                except Exception as e:
                    print(f"Error processing {restaurant_name}: {e}")
                    results.append(f"Error processing {restaurant_name}: {e}")

            return render(request, 'quick_critique_app/bulk.html', {'form': form, 'message': 'Bulk reviews processed.', 'results': results})
    else:
        form = BulkReviewForm()
    return render(request, 'quick_critique_app/bulk.html', {'form': form})