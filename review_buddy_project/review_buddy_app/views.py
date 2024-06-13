from django.shortcuts import render
from .forms import ReviewForm

def index(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            restaurant_name = form.cleaned_data['restaurant_name']
            city_name = form.cleaned_data['city_name']

            # Placeholder for AI processing logic
            
            summary = f"Summary for {restaurant_name} in {city_name}"
            return render(request, 'review_buddy_app/result.html', {'summary': summary})
    else:
        form = ReviewForm()
    return render(request, 'review_buddy_app/index.html', {'form': form})
