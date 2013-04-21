import os
import distutils.dir_util
from datetime import datetime
from django.template import Context, loader, RequestContext
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.conf import settings
from catalog2.media.models import *
from catalog2.camera.models import Catalog
from catalog2.film.models import Life, InCamera
from django.http import HttpResponse, HttpResponseRedirect

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
    previousm = (Media.objects.filter(pk=(int(media_id)-1)) or [None])[0]
    nextm = (Media.objects.filter(pk=(int(media_id)+1)) or [None])[0]
    return render_to_response('media/info.html', {
        'media': media,
        'cameras': media.camera_set.all(),
        'exemples': media.exemple_set.all(),
        'filmsheets': media.filmsheet_set.all(),
        'previous': previousm,
        'next': nextm,
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
        'media': media,
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
        'media': media,
        'exemple': exemple,
    })

@login_required
def media_link_filmsheet(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    incamera = list(InCamera.objects.all())
    incamera.sort(lambda a,b: cmp(a.film_life.reference, b.film_life.reference))
    return render_to_response('media/link_filmsheet.html', {
        'media': media,
        'history': map(lambda h: h.film_life, incamera)
    })

@login_required
def media_linked_filmsheet(request, media_id, life_id):
    media = get_object_or_404(Media, pk=media_id)
    life = get_object_or_404(Life, pk=life_id)
    filmsheet = FilmSheet(film_life=life, media=media)
    filmsheet.save()
    return render_to_response('media/linked_filmsheet.html', {
        'media': media,
        'filmsheet': filmsheet,
    })

def upload(request):
    return render_to_response('media/upload.html',
        context_instance=RequestContext(request, {
    }))

@login_required
@csrf_protect
def do_upload(request):
    for key, file in request.FILES.items():
        path = os.path.join(settings.UPLOAD_PATH, date_path(), file.name)
        distutils.dir_util.mkpath(os.path.dirname(path))
        dest = open(path, 'w')
        if file.multiple_chunks:
            for c in file.chunks():
                dest.write(c)
        else:
            dest.write(file.read())
        dest.close()

    media = Media(
        name=request.POST['name'],
        comment=request.POST['comment'],
        safe=request.POST.get('safe', False),
        url=os.path.join(date_path(), file.name),
    )
    media.save()
    return render_to_response('media/uploaded.html', {
        'media': media,
    })

def date_path():
    now = datetime.now()
    return os.path.join(str(now.year), str(now.month), str(now.day))

def add_tag(request, media_id, tag_id=None):
    media = get_object_or_404(Media, pk=media_id)

    if tag_id:
        tag = get_object_or_404(Tag, pk=tag_id)
        media.tag.add(tag)
        media.save()

    return render_to_response('media/add_tag.html', {
        'media': media,
        'tags': list(set(Tag.objects.all()) - set(media.tags)),
    })

@login_required
def display(request, media_id):
    media = get_object_or_404(Media, pk=media_id)
    if not media.safe:
        return HttpResponseRedirect('/media/')
    if media.url.startswith('http'):
        return HttpResponseRedirect(media.url)
    image = open(os.path.join(settings.UPLOAD_PATH, media.url), 'rb')
    return HttpResponse(image, mimetype='image/jpeg')
