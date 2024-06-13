from django import forms

class ReviewForm(forms.Form):
    restaurant_name = forms.CharField(label='Restaurant Name', max_length=100)
    city_name = forms.CharField(label='City Name', max_length=100)