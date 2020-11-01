import datetime
from dateutil.relativedelta import *
import math
import os

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django_tables2 import RequestConfig
from django.template import loader
from django.http import HttpResponse, JsonResponse

from .forms import SearchForm, DistSearchForm
from .models import Cuisine, MetroArea, District, Restaurant, Picture, Dish
from .tables import RestaurantTable


def filter_restaurants(request):
    # Get all of the objects from the database before filtering
    restaurant_set = Restaurant.objects.order_by('-last_visit')
    restaurant_set = restaurant_set.filter(planned=False)
    cuisine_set = Cuisine.objects.order_by('cuisine_name')
    metroarea_set = MetroArea.objects.order_by('metroarea_name')
    district_set = District.objects.order_by('metroarea__metroarea_name')

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


def filter_restaurants_dist(request, restaurant_set):
    cuisine_filter = request.GET.get('dist_cuisine', '')
    if cuisine_filter and cuisine_filter[0] != '':
        cuisine_filter = cuisine_filter[1:-1].split(',')
        first_cuisine = int(cuisine_filter[0][1:-1])
        cuisine_filter = [int(i[2:-1]) for i in cuisine_filter[1:]]
        cuisine_filter.append(first_cuisine)
        restaurant_set = restaurant_set.filter(cuisine__pk__in=cuisine_filter)

    price_filter = request.GET.get('dist_price', '')
    if price_filter and price_filter[0] != '':
        price_filter = price_filter[1:-1].split(',')
        first_price = len(price_filter[0][1:-1])
        price_filter = [len(i[2:-1]) for i in price_filter[1:]]
        price_filter.append(first_price)
        restaurant_set = restaurant_set.filter(price__in=price_filter)

    metroarea_filter = request.GET.get('dist_metroarea', '')
    if metroarea_filter and metroarea_filter[0] != '':
        metroarea_filter = metroarea_filter[1:-1].split(',')
        first_metroarea = int(metroarea_filter[0][1:-1])
        metroarea_filter = [int(i[2:-1]) for i in metroarea_filter[1:]]
        metroarea_filter.append(first_metroarea)
        restaurant_set = restaurant_set.filter(metroarea__pk__in=metroarea_filter)

    district_filter = request.GET.get('dist_district', '')
    if district_filter and district_filter[0] != '':
        district_filter = district_filter[1:-1].split(',')
        first_district = int(district_filter[0][1:-1])
        district_filter = [int(i[2:-1]) for i in district_filter[1:]]
        district_filter.append(first_district)
        restaurant_set = restaurant_set.filter(Q(district__pk__in=district_filter)|
                                               Q(district__metroarea__pk__in=metroarea_filter))
    return restaurant_set


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


def statistics(request):
    template = loader.get_template('restaurants/statistics.html')
    context = filter_restaurants(request)

    # Compute the average rating and number of restaurants for each cuisine
    cuisines = list(context['cuisines'])
    cuisine_name = []
    cuisine_rating = []
    cuisine_count = []
    other_rating = 0
    other_count = 0
    for cuisine in cuisines:
        filtered_restaurants = context['restaurants'].filter(cuisine=cuisine)
        if len(filtered_restaurants) >= 10:
            cuisine_name.append(cuisine)
            cuisine_count.append(len(filtered_restaurants))
            rat = sum([r.rating for r in filtered_restaurants]) / len(filtered_restaurants)
            rat = int(rat * 100) / 100
            cuisine_rating.append(rat)
        elif len(filtered_restaurants) > 0:
            other_rating += sum([r.rating for r in filtered_restaurants])
            other_count += len(filtered_restaurants)
    cuisine_data = [(cuisine_name[i], cuisine_rating[i], cuisine_count[i]) for i in range(len(cuisine_name))]
    other_rating = int(other_rating / other_count * 100) / 100
    cuisine_data.append(("Other", other_rating, other_count))

    form = DistSearchForm(request.GET)
    context = {
        'google_api_key': os.environ['GOOGLE_API_KEY'],
        'cuisine_data': cuisine_data,
        'dist_cuisine': request.GET.getlist('dist_cuisine', ''),
        'dist_price': request.GET.getlist('dist_price', ''),
        'dist_metroarea': request.GET.getlist('dist_metroarea', ''),
        'dist_district': request.GET.getlist('dist_district', ''),
        'cuisines': context['cuisines'],
        'metroareas': context['metroareas'],
        'districts': context['districts'],
        'form': form
    }
    return HttpResponse(template.render(context))


def get_statistics_data(request):
    context = filter_restaurants(request)

    # Compute the distribution of ratings
    ratings = list(range(1, 11))
    rating_counts = []
    dist_restaurant_set = filter_restaurants_dist(request, context['restaurants'])
    for rating in ratings:
        filtered_restaurants = dist_restaurant_set.filter(rating=int(rating))
        rating_counts.append(len(filtered_restaurants))

    average_rating = sum([i * rating_counts[i-1] for i in range(1, 11)]) / sum(rating_counts)
    average_rating = int(average_rating * 100) / 100
    stddev_rating = math.sqrt(sum([rating_counts[i-1] * (i - average_rating) ** 2 for i in range(1, 11)]) / sum(rating_counts))
    stddev_rating = int(stddev_rating * 100) / 100
    total_rated = sum(rating_counts)
    ratings.reverse()
    rating_counts.reverse()

    # Compute the average rating and number of restaurants for each metroarea
    metroareas = list(context['metroareas'])
    metroarea_rating = []
    metroarea_count = []
    for metroarea in metroareas:
        filtered_restaurants = context['restaurants'].filter(metroarea=metroarea)
        if len(filtered_restaurants) > 0:
            metroarea_count.append(len(filtered_restaurants))
            rat = sum([r.rating for r in filtered_restaurants]) / len(filtered_restaurants)
            rat = int(rat * 100) / 100
            metroarea_rating.append(rat)
    metroareas = [m.metroarea_name for m in list(context['metroareas'])]
    metroarea_address = [m.address for m in list(context['metroareas'])]

    # Compute the number of restaurants in each month of the last three years
    # Restaurant.last_visit: models.DateField(blank=True, null=True)
    curr_month = datetime.datetime.today().month
    curr_year = datetime.datetime.today().year
    month_counts = []
    months = []
    month_to_str = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
                    7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}
    for i in range(36):
        start_date = datetime.date(curr_year, curr_month, 1)
        end_date = start_date + relativedelta(months=+1)
        filtered_restaurants = context['restaurants'].filter(
                last_visit__gte=start_date,
                last_visit__lt=end_date)
        month_counts.append(len(filtered_restaurants))
        months.append("{} {}".format(month_to_str[curr_month], curr_year))
        if (curr_month == 1):
            curr_month = 12
            curr_year -= 1
        else:
            curr_month -= 1
    month_counts.reverse()
    months.reverse()

    data = {
        "ratings_labels": ratings,
        "ratings_default": rating_counts,
        "total_rated": total_rated,
        "average_rating": average_rating,
        "stddev_rating": stddev_rating,
        "metroareas": metroareas,
        "metroarea_address": metroarea_address,
        "metroarea_rating": metroarea_rating,
        "metroarea_count": metroarea_count,
        "months": months,
        "month_counts": month_counts,
        "dist_metroarea": request.GET.get('dist_metroarea', '')
    }
    return JsonResponse(data)
