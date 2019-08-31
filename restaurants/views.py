import os

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_tables2 import RequestConfig
from django.template import loader
from django.http import HttpResponse

from .forms import SearchForm
from .models import Cuisine, MetroArea, District, Restaurant, Picture, Dish
from .tables import RestaurantTable


def filter_restaurants(request):
    # Get all of the objects from the database before filtering
    restaurant_set = Restaurant.objects.order_by('-last_visit')
    restaurant_set = restaurant_set.filter(planned=False)
    cuisine_set = Cuisine.objects.order_by('cuisine_name')
    metroarea_set = MetroArea.objects.order_by('metroarea_name')
    district_set = District.objects.order_by('metroarea_name')

    # Restaurant name filtering
    name_filter = request.GET.get('name', '')
    if name_filter:
        restaurant_set = restaurant_set.filter(restaurant_name__icontains=name_filter)

    # Minimum rating filtering
    rating_filter = request.GET.get('rating', '')
    if rating_filter:
        restaurant_set = restaurant_set.filter(rating__gte=int(rating_filter))

    # Cuisine filtering
    cuisine_filter = request.GET.getlist('cuisine', '')
    if cuisine_filter:
        cuisine_filter = [int(i) for i in cuisine_filter]
        restaurant_set = restaurant_set.filter(cuisine__pk__in=cuisine_filter)

    # Price filtering
    price_filter = request.GET.getlist('price', '')
    if price_filter:
        price_filter = [len(p) for p in price_filter]
        restaurant_set = restaurant_set.filter(price__in=price_filter)

    # Metroarea filtering
    metroarea_filter = request.GET.getlist('metroarea', '')
    if metroarea_filter:
        metroarea_filter = [int(i) for i in metroarea_filter]
        restaurant_set = restaurant_set.filter(metroarea__pk__in=metroarea_filter)

    # District filtering
    # Note: If a metroarea is selected, it by default selects all districts 
    #       within that metroarea, regardless of whether districts are selected
    district_filter = request.GET.getlist('district', '')
    if district_filter:
        district_filter = [int(i) for i in district_filter]
        restaurant_set = restaurant_set.filter(Q(district__pk__in=district_filter)|
                                               Q(district__metroarea__pk__in=metroarea_filter))

    # Return the object for further processing to the view function
    context = {
        'request': request,
        'restaurants': restaurant_set,
        'cuisines': cuisine_set,
        'metroareas': metroarea_set,
        'districts': district_set
    }
    return context


def index(request):
    template = loader.get_template('restaurants/index.html')
    context = filter_restaurants(request)
    form = SearchForm(request.GET)
    table = RestaurantTable(context['restaurants'])
    RequestConfig(request).configure(table)
    context['form'] = form
    context['table'] = table
    return HttpResponse(template.render(context))


def details(request, url_name):
    restaurant = get_object_or_404(Restaurant, url_name=url_name)
    pictures = reversed(Picture.objects.filter(restaurant=restaurant))
    dishes = reversed(Dish.objects.filter(restaurant=restaurant))
    template = loader.get_template('restaurants/details.html')
    context = {
        'request': request,
        'url_name': url_name, 
        'restaurant': restaurant,
        'pictures': pictures,
        'dishes': list(dishes),
        'google_api_key': os.environ['GOOGLE_API_KEY'],
    }
    return HttpResponse(template.render(context))
