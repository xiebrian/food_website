from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse

def index(request):
    template = loader.get_template('personal/index.html')
    context = {}
    return HttpResponse(template.render(context))
