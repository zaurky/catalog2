# Create your views here.
from catalog2.film.models import Catalog, Life, InCamera, Sensitivity
from catalog2.camera.models import Catalog as CameraCatalog
from catalog2.contact.models import Developer
from catalog2.develop.models import Product

from django.shortcuts import render_to_response, get_object_or_404

def stats(request):
    return render_to_response('stats/info.html', {
        'camera_num': CameraCatalog.objects.count(),
        'film_num': InCamera.objects.count(),
        'total_price': CameraCatalog.total_sum(),
    })
