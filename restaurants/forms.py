from django import forms

from .models import Cuisine, MetroArea, District


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
