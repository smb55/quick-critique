from celery import shared_task
from .scraping import generate_review_data

@shared_task
def process_bulk_reviews(city_name, restaurant_names):
    results = []
    for restaurant_name in restaurant_names:
        try:
            print("Processing:", restaurant_name)
            generate_review_data(restaurant_name, city_name)
            results.append(f"{restaurant_name} processed successfully.")
        except Exception as e:
            print(f"Error processing {restaurant_name}: {e}")
            results.append(f"Error processing {restaurant_name}: {e}")
    return results
