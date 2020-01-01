from django.template import loader
from django.http import HttpResponse

# Create your views here.

def index(request):
    template = loader.get_template('h31mp/index.html')
    context = {}
    return HttpResponse(template.render(context))
