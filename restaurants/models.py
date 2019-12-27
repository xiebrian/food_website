import os

from pathlib import Path

from django.db import models
from django.urls import reverse


class Cuisine(models.Model):
    """ Represents a cuisine (e.g. Italian, Seafood, etc) """
    cuisine_name = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.cuisine_name


class MetroArea(models.Model):
    """ Represents a metropolitan area (e.g. Boston, New York, Other) """
    metroarea_name = models.CharField(max_length=100, unique=True)
    address = models.CharField(max_length=100)
    def __str__(self):
        return self.metroarea_name


class District(models.Model):
    """ Represents a district within a metropolitan area (e.g. East Village) """
    district_name = models.CharField(max_length=100, unique=False)
    metroarea     = models.ForeignKey(MetroArea, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.metroarea) + ": " + self.district_name

    class Meta:
        ordering = ('metroarea__metroarea_name', 'district_name')


class Restaurant(models.Model):
    """ Django class representing all relevant information for a restaurant. """
    # Basic restaurant information
    restaurant_name = models.CharField(max_length=100)
    cuisine         = models.ManyToManyField(to=Cuisine, blank=True)
    price           = models.IntegerField(
                          choices = ((1, '$'), (2, '$$'), (3, '$$$'), (4, '$$$$'), (5, '$$$$$'), (6, '$$$$$$')),
                          default = 1,
                          help_text = "$ = <10, $$ = 11-20, $$$ = 21-30, $$$$ = 31-50, $$$$$ = 51-100, $$$$$$ = >100")

    # Location information
    metroarea       = models.ForeignKey(MetroArea, on_delete=models.CASCADE)
    district        = models.ForeignKey(District, on_delete=models.CASCADE)
    address         = models.CharField(max_length=300)

    # Personal review of the restaurant
    rating          = models.IntegerField(
                          choices = [(i, i) for i in range(1, 11)],
                          default = 5,
                          blank=True,
                          null=True)
    positives       = models.TextField("Positives", default="", blank=True)
    negatives       = models.TextField("Negatives", default="", blank=True)
    notes           = models.TextField("Notes", default="", blank=True)
    private_notes   = models.TextField("Private Notes", default="", blank=True)

    # Logistical information
    last_visit      = models.DateField(blank=True, null=True) 
    url_name        = models.SlugField(max_length=50, unique=True)
    planned         = models.BooleanField(default=False)

    # Used to display cuisine in the admin form
    def cuisines(self):
        return ", ".join([str(cuisine) for cuisine in self.cuisine.all()])

    def __str__(self):
        return self.restaurant_name

    def details(self):
        return u"\U0001F517"

    def get_absolute_url(self):
        return "/restaurants/%s/" % self.url_name


def picture_file_name(instance, filename):
    ext = Path(filename).suffix
    name = str(instance.restaurant) + '_' + instance.caption + ext
    return os.path.join('restaurant_pictures', name)


class Picture(models.Model):
    """ Represents a picture. Must be associated with some restaurant. """
    picture = models.ImageField(upload_to=picture_file_name, 
                    help_text="Remember to crop the image into a square!")
    caption = models.CharField(max_length=200)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.restaurant) + ': ' + self.caption


class Dish(models.Model):
    """ Represents a single dish at a restaurant """
    dish_name  = models.CharField(max_length=100, unique=False)
    rating     = models.IntegerField(
                        choices = ((0, 0), (1, 1), (2, 2), (3, 3), (4, 4)),
                        default = 0)
    notes      = models.CharField(max_length=500, blank=True, unique=False)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return str(self.dish_name)
