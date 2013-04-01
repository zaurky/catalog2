# Create your views here.
from catalog2.film.models import Catalog, Life, InCamera, Sensitivity, Ref
from catalog2.camera.models import (Catalog as CameraCatalog,
    Model as CameraModel)
from catalog2.lens.models import Catalog as LensCatalog

from catalog2.contact.models import Developer
from catalog2.develop.models import Product

from django.shortcuts import render_to_response, get_object_or_404

def stats(request):
    return render_to_response('stats/info.html', {
        'camera_num': CameraCatalog.objects.count(),
        'camera_model': CameraModel.objects.count(),
        'film_num': Life.objects.count(),
        'film_ref': Ref.objects.count(),
        'film_done': InCamera.objects.count(),
        'total_price': CameraCatalog.total_sum() + LensCatalog.total_sum(),
        'total_camera_price': CameraCatalog.total_sum(),
        'total_lens_price': LensCatalog.total_sum(),
    })
