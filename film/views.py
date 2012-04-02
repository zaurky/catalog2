from django.template import Context, loader
from catalog2.film.models import Catalog, Life
from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404

# Create your views here.

def list(request):
    catalog_list = Catalog.objects.all()
    t = loader.get_template('film/list.html')
    c = Context({
        'catalog_list': catalog_list,
    })
    return HttpResponse(t.render(c))

def info(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    filmlife = Life.objects.filter(film_catalog=catalog)
    return render_to_response('film/info.html', {
        'catalog': catalog,
        'filmlife': filmlife,
    })

def edit(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    return render_to_response('film/edit.html', {
        'catalog': catalog,
    })

def update(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
