from django.template import Context, loader
from catalog2.camera.models import Catalog
from django.http import HttpResponse

# Create your views here.

def list(request):
    catalog_list = Catalog.objects.all()
    t = loader.get_template('camera/list.html')
    c = Context({
        'catalog_list': catalog_list,
    })
    return HttpResponse(t.render(c))

def info(request, catalog_id):
    return
