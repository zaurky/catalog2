from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import Context, loader, RequestContext
from django.views.decorators.csrf import csrf_protect

from catalog2.lens.models import Catalog

# Create your views here.

def catalog_list(request):
    return render_to_response('lens/list.html', {
        'catalog_list': Catalog.objects.all(),
    })


def catalog_info(request, lens_id):
    return render_to_response('lens/info.html', {
        'catalog': get_object_or_404(Catalog, pk=lens_id),
    })


@login_required
def catalog_sell(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    return render_to_response('lens/sell.html',
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
    return render_to_response('lens/selling.html',
        context_instance=RequestContext(request, {'catalog': catalog}))


@login_required
def catalog_sold(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    catalog.sold()
    catalog.save()
    return HttpResponseRedirect('/lens/catalog/%s' % catalog_id)
