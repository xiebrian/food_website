import os
import datetime

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.template import loader
from django.http import HttpResponse
from .models import Recipe, Category, Ingredient, Cuisine

from django.core.paginator import Paginator


def filter_recipes(request):
    recipe_set = Recipe.objects.order_by('recipe_name')

    # Type filtering (Featured, Recent, Short Time, Long Time)
    type_filter = request.GET.get('type', '')
    if type_filter:
        if type_filter == 'recent':
            recipe_set = recipe_set.order_by('-last_cook_time')[:25]
        elif type_filter == 'featured':
            # TODO: uncomment this when the migration is done
            # recipe_set = recipe_set.filter(~Q(feature_position=0)).order_by('recipe_name')
        elif type_filter == 'short-time':
            recipe_set = recipe_set.order_by('total_time').filter(
                                    total_time__lte=datetime.timedelta(hours=1))
        elif type_filter == 'long-time':
            recipe_set = recipe_set.order_by('-total_time').filter(
                                    total_time__gte=datetime.timedelta(hours=1))

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

    # Pagination
    paginator = Paginator(recipes_to_display, 25)
    page_number = request.GET.get("page")
    if page_number is None:
        page_number = 1
    recipes_to_display_paginated = paginator.get_page(page_number)
    page_range = paginator.get_elided_page_range(page_number, on_each_side=3, on_ends=1)

    context = {
        'recipes_to_display': recipes_to_display_paginated,
        'current_page_number': int(page_number),
        'page_range': page_range,
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
