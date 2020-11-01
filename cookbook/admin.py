from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from image_cropping import ImageCroppingMixin

from .models import Recipe, Ingredient, Category, Cuisine
from .forms import RecipeChangeListForm


class RecipeChangeList(ChangeList):
    def __init__(self, request, model, list_display, list_display_links,
                 list_filter, date_hierarchy, search_fields,
                 list_select_related, list_per_page, list_max_show_all,
                 list_editable, model_admin, sortable_by):

        super(RecipeChangeList, self).__init__(
                request, model, list_display, list_display_links,
                list_filter, date_hierarchy, search_fields,
                list_select_related, list_per_page, list_max_show_all,
                list_editable, model_admin, sortable_by)

        # self.list_display = ['action_checkbox', 'recipe_name']
        # self.list_display_links = ['recipe_name']
        # self.list_editable = []


class RecipeAdmin(ImageCroppingMixin, admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return RecipeChangeList

    def get_changelist_form(self, request, **kwargs):
        return RecipeChangeListForm

    fieldsets = [
        (None, {'fields': ['recipe_name', 'picture', 'cropping']}),
        ('Recipe Description', {'fields': ['desc_summary', 'text_ingred', 'instructions', 'notes', 'personal_log']}),
        ('Recipe Information', {'fields': ['ingredients', 'cooking_time', 'total_time', 'categories', 'cuisines']}),
        ('Logging Information', {'fields': ['last_cook_time', 'number_of_attempts', 'is_experiment', 'feature_position', 'url_name']})
    ]
    list_display = ('recipe_name', 'cooking_time', 'total_time', 'is_experiment')
    search_fields = ['categories__category_name',
                     'cuisines__cuisine_name',
                     'ingredients__ingredient_name',
                     'recipe_name']
    filter_horizontal = ('categories', 'ingredients', 'cuisines')


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(Cuisine)
