from django import forms
from .models import Ingredient, Category


class RecipeChangeListForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
                         queryset=Category.objects.all(),
                         required=True
                 )
