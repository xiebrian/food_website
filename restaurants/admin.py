from django.contrib import admin

from .models import Restaurant, Picture, Cuisine, MetroArea, District, Dish


class PicturesInline(admin.StackedInline):
    model = Picture
    extra = 0
    insert_after = 'private_notes'


class DishesInline(admin.StackedInline):
    model = Dish
    extra = 0
    insert_after = 'negatives'


class RestaurantAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['restaurant_name', 'cuisine', 'price']}),
        ('Review Information', {'fields': ['rating', 'notes', 'positives', 'negatives', 'private_notes']}),
        ('Location Information', {'fields': ['metroarea', 'district', 'address']}),
        ('Logistical Information', {'fields': ['last_visit', 'url_name', 'planned']})
    ]
    list_display = ['restaurant_name', 'rating', 'cuisines', 'price', 'district', 'planned']
    search_fields = [
        'restaurant_name',
        'metroarea__metroarea_name',
        'district__district_name',
        'cuisine__cuisine_name'
    ]
    filter_horizontal = ['cuisine']
    inlines = [PicturesInline, DishesInline]
    change_form_template = 'admin/custom/change_form.html'

    class Media:
        css = {'all': ('admin.css',)}


class PictureAdmin(admin.ModelAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'restaurant':
            kwargs['queryset'] = Restaurant.objects.order_by('restaurant_name')
        return super(PictureAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        return Picture.objects.order_by('restaurant__restaurant_name')


class CuisineAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return Cuisine.objects.order_by('cuisine_name')


class MetroAreaAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return MetroArea.objects.order_by('metroarea_name')


class DistrictAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        return District.objects.order_by('metroarea__metroarea_name')


# Register your models here.
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Picture, PictureAdmin)
admin.site.register(Cuisine, CuisineAdmin)
admin.site.register(MetroArea, MetroAreaAdmin)
admin.site.register(District, DistrictAdmin)
