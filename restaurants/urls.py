from django.urls import path

from . import views

app_name = 'restaurants'
urlpatterns = [
    path('', views.index, name='index'),
    path('statistics/', views.statistics, name='statistics'),
    path('api/statistics/data/', views.get_statistics_data, name='api-data'),
    path('<slug:url_name>/', views.details, name='details')
]
