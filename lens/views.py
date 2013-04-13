from catalog2.lens.models import Catalog

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def catalog_list(request):
    return render_to_response('lens/list.html', {
        'catalog_list': Catalog.objects.all(),
    })


def catalog_info(request, lens_id):
    return render_to_response('lens/info.html', {
        'catalog': get_object_or_404(Catalog, pk=lens_id),
    })
