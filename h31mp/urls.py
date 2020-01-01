from django.urls import path

from . import views

app_name = 'h31mp'
urlpatterns = [
    path('', views.index, name='index')
]
