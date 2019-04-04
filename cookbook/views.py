import os

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Recipe, Category, Ingredient, Cuisine


def filter_recipes(request):
    recipe_set = Recipe.objects.order_by('recipe_name')

    # Type filtering (Featured, Recent, Experiments)
    type_filter = request.GET.get('type', '')
    if type_filter:
        if type_filter == 'featured':
            recipe_set = recipe_set.filter(~Q(feature_position=0))
        elif type_filter == 'recent':
            recipe_set = recipe_set.order_by('-last_cook_time')[:5]
        elif type_filter == 'experiments':
            recipe_set = recipe_set.filter(is_experiment=True)

    # Cuisine filtering 
    cuisine_filter = request.GET.get('cuisine', '')
    if cuisine_filter:
        recipe_set = recipe_set.filter(cuisines__cuisine_name__contains=cuisine_filter)

    # Category filtering
    category_filter = request.GET.get('category', '')
    if category_filter:
        recipe_set = recipe_set.filter(categories__category_name__contains=category_filter)

    # Main Ingredient filter
    ingredient_filter = request.GET.get('ingredient', '')
    if ingredient_filter:
        recipe_set = recipe_set.filter(ingredients__ingredient_name__contains=ingredient_filter)
   
    return recipe_set


def index(request):
    recipes_to_display = filter_recipes(request)
    template = loader.get_template('cookbook/index.html')
    cuisines = Cuisine.objects.order_by('cuisine_name')
    categories = Category.objects.order_by('category_name')
    main_ingredients = Ingredient.objects.order_by('ingredient_name')
    context = {
        'recipes_to_display': recipes_to_display,
        'cuisines': cuisines,
        'categories': categories,
        'main_ingredients': main_ingredients
    }
    return HttpResponse(template.render(context))


def details(request, url_name):
    recipe = get_object_or_404(Recipe, url_name=url_name)
    template = loader.get_template('cookbook/details.html')
    context = {'url_name': url_name, 'recipe': recipe}
    return HttpResponse(template.render(context))
