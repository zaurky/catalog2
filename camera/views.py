from django.template import Context, loader
from catalog2.camera.models import Catalog
from catalog2.film.models import InCamera as FilmInCamera
from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.

def list(request):
    catalog_list = Catalog.objects.all()
    t = loader.get_template('camera/list.html')
    c = Context({
        'catalog_list': catalog_list,
    })
    return HttpResponse(t.render(c))

def info(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    filmincamera = FilmInCamera.objects.filter(camera_catalog=catalog, loaded=1)
    history = FilmInCamera.objects.filter(camera_catalog=catalog, loaded=0)
    return render_to_response('camera/info.html', {
        'catalog': catalog,
        'filmincamera': filmincamera,
        'history': history,
    })
