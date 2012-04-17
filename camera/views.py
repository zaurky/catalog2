from catalog2.camera.models import Catalog
from catalog2.film.models import InCamera as FilmInCamera

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def catalog_list(request):
    catalog_list = Catalog.objects

    if request.GET.get('best'):
        catalog_list = list(catalog_list.filter(incamera__isnull=False).distinct())
        catalog_list.sort(lambda b,a:
            cmp(a.num_films, b.num_films) or cmp(unicode(b), unicode(a)))
    else:
        catalog_list = catalog_list.all()

    if request.GET.get('loaded'):
        catalog_list = filter(lambda c: c.loaded, catalog_list)

    return render_to_response('camera/list.html', {
        'catalog_list': catalog_list,
    })

@login_required
def catalog_info(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    history = FilmInCamera.objects.filter(camera_catalog=catalog, loaded=0)
    return render_to_response('camera/info.html', {
        'catalog': catalog,
        'history': history,
        'encyclopedias': catalog.camera_model.encyclopedia,
    })

@login_required
def catalog_edit(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    return render_to_response('camera/edit.html', {
        'catalog': catalog,
    })

@login_required
def catalog_update(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
