from django.urls import path
from .views import index, bulk_reviews

urlpatterns = [
    path('', index, name='index'),
    path('bulk/', bulk_reviews, name='bulk_reviews')
]