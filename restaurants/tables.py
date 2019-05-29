import django_tables2 as tables

from .models import Restaurant

class RestaurantTable(tables.Table):
    class Meta:
        model = Restaurant
        template_name = 'django_tables2/bootstrap4.html'
        fields = ['restaurant_name', 'cuisines', 'price', 'district', 'last_visit', 'rating', 'details']

    restaurant_name = tables.Column(initial_sort_descending=True)
    cuisines = tables.Column(orderable=False)
    rating = tables.Column(attrs=
        {'th': {'style': 'text-align: center;'}, 'td': {'align': 'center'}})
    details = tables.Column(orderable=False, linkify=True, attrs=
        {'th': {'style': 'text-align: center;'},'td': {'align': 'center'}}) 
