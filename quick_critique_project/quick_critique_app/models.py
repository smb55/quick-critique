from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    display_name = models.CharField(max_length=255, null=True, blank=True)
    rating = models.FloatField(null=True, blank=True)
    user_rating_count = models.IntegerField(null=True, blank=True)
    place_id = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"{self.display_name} in {self.city}"


class ReviewSummary(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    food = models.TextField()
    service = models.TextField()
    atmosphere = models.TextField()
    price = models.TextField()
    trend = models.TextField()
    summary = models.TextField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Summary for {self.restaurant.display_name}"
