import os
import datetime

from pathlib import Path

from django.db import models


def picture_file_name(instance, filename):
    ext = Path(filename).suffix
    name = instance.recipe_name + ext
    return os.path.join('food_pictures', name)


class Category(models.Model):
    """ Represents a category for a recipe (e.g. Italian, Seafood, Dessert) """
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Ingredient(models.Model):
    """ Represents a main ingredient used in a recipe """
    ingredient_name = models.CharField(max_length=100)

    def __str__(self):
        return self.ingredient_name


class Recipe(models.Model):
    """
    Django class representing all relevant information for a recipe.
    """
    recipe_name  = models.CharField(max_length=100)
    picture      = models.ImageField(blank=True, upload_to=picture_file_name)

    description  = models.TextField(default="")
    ingredients  = models.ManyToManyField(to=Ingredient)
    cooking_time = models.DurationField(default=datetime.timedelta())
    total_time   = models.DurationField(default=datetime.timedelta())
    categories   = models.ManyToManyField(to=Category)

    last_cook_time = models.DateField()
    number_of_attempts = models.IntegerField(
        choices = ((0, '0'), (1, '1'), (2, '2'), (3, '3'), (4, '>3')),
        default = 0
    )
    mastery = models.BooleanField(default=False)
    feature_position = models.IntegerField(default=0)

    def __str__(self):
        return self.recipe_name
