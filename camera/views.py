from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_protect

from catalog2.camera.models import Catalog
from catalog2.film.models import InCamera as FilmInCamera

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

    template = 'list.html'
    if request.is_ajax():
        template = 'ajax_%s' % template

    return render_to_response('camera/%s' % template, {
        'catalog_list': catalog_list,
    })

@login_required
def catalog_info(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    history = list(FilmInCamera.objects.filter(camera_catalog=catalog, loaded=0))
    history.sort()
    return render_to_response('camera/info.html', {
        'catalog': catalog,
        'history': history,
        'encyclopedias': catalog.camera_model.encyclopedia,
        'media': catalog.camera_model.media.all(),
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


@login_required
def catalog_sell(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    return render_to_response('camera/sell.html',
        context_instance=RequestContext(request, {'catalog': catalog}))


@login_required
@csrf_protect
def catalog_selling(request):
    catalog = get_object_or_404(Catalog, pk=request.POST.get('catalog_id'))
    catalog.selling(
        request.POST.get('price'),
        request.POST.get('comment'),
    )
    catalog.save()
    return render_to_response('camera/selling.html',
        context_instance=RequestContext(request, {'catalog': catalog}))


@login_required
def catalog_sold(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    catalog.sold()
    catalog.save()
    return HttpResponseRedirect('/camera/catalog/%s' % catalog_id)
