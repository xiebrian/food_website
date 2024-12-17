import os
import datetime

from pathlib import Path
from image_cropping import ImageRatioField

from django.db import models


def picture_file_name(instance, filename):
    ext = Path(filename).suffix
    name = instance.recipe_name + ext
    return os.path.join('food_pictures', name)


class Cuisine(models.Model):
    """ Represents a cuisine (e.g. Italian, Seafood, etc) """
    cuisine_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.cuisine_name


class Category(models.Model):
    """ Represents a category or cooking technique (e.g. braise)"""
    category_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category_name


class Ingredient(models.Model):
    """ Represents a main ingredient used in a recipe """
    ingredient_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.ingredient_name


class Recipe(models.Model):
    """
    Django class representing all relevant information for a recipe.
    """
    recipe_name  = models.CharField(max_length=100)
    picture      = models.ImageField(blank=True, upload_to=picture_file_name)
    cropping     = ImageRatioField('picture', '1000x1000', size_warning=True)

    desc_summary = models.TextField("Description Summary", default="", blank=True)
    text_ingred  = models.TextField("Ingredients List", default="", blank=True)
    instructions = models.TextField("Instructions", default="", blank=True)
    notes        = models.TextField("Notes and Tips", default="", blank=True)
    personal_log = models.TextField("Personal Notes", default="", blank=True)

    cuisines    = models.ManyToManyField(to=Cuisine, blank=True)
    ingredients = models.ManyToManyField(to=Ingredient, blank=True)
    active_time = models.DurationField(default=datetime.timedelta())
    total_time  = models.DurationField(default=datetime.timedelta())
    categories  = models.ManyToManyField(to=Category, blank=True)

    last_cook_time = models.DateField()
    number_of_attempts = models.IntegerField(
        choices = ((0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '>3')),
        default = 0
    )
    featured = models.BooleanField(default=False)
    url_name = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.recipe_name
