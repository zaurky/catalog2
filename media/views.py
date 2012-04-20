from catalog2.media.models import *
from catalog2.camera.models import Catalog
from catalog2.film.models import Life, InCamera

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.
def media_list(request):
    media_list = Media.objects.all()
    return render_to_response('media/list.html', {
        'media_list': media_list,
    })

@login_required
def media_info(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    return render_to_response('media/info.html', {
        'media': media,
        'cameras': Camera.objects.all(),
        'exemples': Exemple.objects.all(),
    })

@login_required
def media_link_camera(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    return render_to_response('media/link_camera.html', {
        'media': media,
        'camera_catalogs': Catalog.objects.all(),
    })

@login_required
def media_linked_camera(request, media_id, catalog_id):
    media = get_object_or_404(Media, pk=media_id)
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    camera = Camera(camera_model=catalog.camera_model, media=media)
    camera.save()
    return render_to_response('media/linked_camera.html', {
        'camera': camera,
    })

@login_required
def media_link_exemple(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    incamera = list(InCamera.objects.all())
    incamera.sort(lambda a,b: cmp(a.film_life.reference, b.film_life.reference))
    return render_to_response('media/link_exemple.html', {
        'media': media,
        'history': map(lambda h: h.film_life, incamera)
    })

@login_required
def media_linked_exemple(request, media_id, life_id):
    media = get_object_or_404(Media, pk=media_id)
    life = get_object_or_404(Life, pk=life_id)
    exemple = Exemple(film_life=life, media=media)
    exemple.save()
    return render_to_response('media/linked_exemple.html', {
        'exemple': exemple,
    })
