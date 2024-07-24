from celery import shared_task
from .scraping import generate_review_data
import concurrent.futures


@shared_task
def process_bulk_reviews(city_name, restaurant_names):
    results = []

    def process_restaurant(restaurant_name):
        try:
            print("Processing:", restaurant_name)
            generate_review_data(restaurant_name, city_name)
            return f"{restaurant_name} processed successfully."
        except Exception as e:
            print(f"Error processing {restaurant_name}: {e}")
            return f"Error processing {restaurant_name}: {e}"

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_restaurant = {executor.submit(process_restaurant, restaurant_name): restaurant_name for restaurant_name in restaurant_names}
        for future in concurrent.futures.as_completed(future_to_restaurant):
            restaurant_name = future_to_restaurant[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                print(f"Error processing {restaurant_name}: {e}")
                results.append(f"Error processing {restaurant_name}: {e}")

    return results
