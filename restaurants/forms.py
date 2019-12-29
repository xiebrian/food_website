from django import forms

from .models import Restaurant, Cuisine, MetroArea, District

class SearchForm(forms.Form):
    name = forms.CharField(
            label='Restaurant Name', 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 10}),
            max_length=100, 
            required=False)
    rating = forms.IntegerField(
            label='Minimum Rating', 
            min_value=1, 
            max_value=10, 
            widget=forms.NumberInput(attrs={'style': 'width:6ch'}),
            required=False)
    cuisine = forms.ModelMultipleChoiceField(
            queryset=Cuisine.objects.order_by('cuisine_name'),
            required=False,
            widget=forms.CheckboxSelectMultiple)
    price = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$'), 
                ('$$$$', '$$$$'), ('$$$$$', '$$$$$'), ('$$$$$$', '$$$$$$')])
    metroarea = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            queryset=MetroArea.objects.order_by('metroarea_name'))
    district = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            queryset=District.objects.order_by('district_name'))

# Include only cuisines which have >= 10 restaurants
restaurants = Restaurant.objects.filter(planned=False)
cuisines = Cuisine.objects.order_by('cuisine_name')
filtered_cuisines = []
for cuisine in cuisines:
    if len(restaurants.filter(cuisine=cuisine)) >= 10:
        filtered_cuisines.append(cuisine.cuisine_name)
cuisine_queryset = cuisines.filter(cuisine_name__in=filtered_cuisines)

class DistSearchForm(forms.Form):
    name = forms.CharField(
            label='Restaurant Name', 
            widget=forms.Textarea(attrs={'rows': 1, 'cols': 10}),
            max_length=100, 
            required=False)
    rating = forms.IntegerField(
            label='Minimum Rating', 
            min_value=1, 
            max_value=10, 
            widget=forms.NumberInput(attrs={'style': 'width:6ch'}),
            required=False)
    cuisine = forms.ModelMultipleChoiceField(
            queryset=cuisine_queryset,
            required=False,
            widget=forms.CheckboxSelectMultiple)
    price = forms.MultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            choices=[('$', '$'), ('$$', '$$'), ('$$$', '$$$'), 
                ('$$$$', '$$$$'), ('$$$$$', '$$$$$'), ('$$$$$$', '$$$$$$')])
    metroarea = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            queryset=MetroArea.objects.order_by('metroarea_name'))
    district = forms.ModelMultipleChoiceField(
            required=False,
            widget=forms.CheckboxSelectMultiple,
            queryset=District.objects.order_by('district_name'))
