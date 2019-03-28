from django.contrib import admin
from django.contrib.admin.views.main import ChangeList

from .models import Recipe, Ingredient, Category
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


class RecipeAdmin(admin.ModelAdmin):
    def get_changelist(self, request, **kwargs):
        return RecipeChangeList

    def get_changelist_form(self, request, **kwargs):
        return RecipeChangeListForm

    fieldsets = [
        (None, {'fields': ['recipe_name', 'picture']}),
        ('Recipe Information', {'fields': ['description', 'ingredients', 'cooking_time', 'total_time', 'categories']}),
        ('Logging Information', {'fields': ['last_cook_time', 'number_of_attempts', 'mastery', 'feature_position']})
    ]
    list_display = ('recipe_name', 'cooking_time', 'total_time', 'mastery')
    search_fields = ['categories__category_name', 
                     'ingredients__ingredient_name',
                     'recipe_name']


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient)
admin.site.register(Category)
