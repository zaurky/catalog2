from django.template import Context, loader, RequestContext
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from catalog2.film.models import Catalog, Life, InCamera
from catalog2.camera.models import Catalog as CameraCatalog
from catalog2.contact.models import Developer
from django.http import HttpResponse

from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required

# Create your views here.

def catalog_list(request):
    catalog_list = Catalog.objects.all()
    t = loader.get_template('film/list.html')
    c = Context({
        'catalog_list': catalog_list,
    })
    return HttpResponse(t.render(c))

@login_required
def catalog_info(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    filmlife = Life.objects.filter(film_catalog=catalog)
    return render_to_response('film/info.html', {
        'catalog': catalog,
        'filmlife': filmlife,
    })

@login_required
def catalog_edit(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)
    return render_to_response('film/edit.html', {
        'catalog': catalog,
    })

@login_required
def catalog_update(request, catalog_id):
    catalog = get_object_or_404(Catalog, pk=catalog_id)

@login_required
def life_view(request, life_id):
    life = get_object_or_404(Life, pk=life_id)
    return render_to_response('film/life_info.html', {
        'life': life,
        'incamera': (life.incamera.all() or [None])[0],
        'products': life.products.all()
    })

@login_required
def incamera_camera_load(request, camera_catalog_id):
    camera_catalog = get_object_or_404(CameraCatalog, pk=camera_catalog_id)
    film_catalogs = Catalog.objects.all()
    return render_to_response('incamera/load_film.html', {
        'camera_catalog': camera_catalog,
        'film_catalogs': film_catalogs,
    })

@login_required
def incamera_camera_unload(request, camera_catalog_id):
    camera_catalog = get_object_or_404(CameraCatalog, pk=camera_catalog_id)
    if not camera_catalog.loaded:
        raise

    incamera = camera_catalog.loaded
    life = incamera.film_life

    incamera.unload(life.film_catalog.poses)
    life.unload()

    incamera.save()
    life.save()

    return render_to_response('incamera/unloaded.html', {
        'incamera': incamera,
    })

@login_required
def incamera_film_load(request, life_id):
    life = get_object_or_404(Life, pk=life_id)
    camera_catalogs = CameraCatalog.objects.all()
    return render_to_response('incamera/load_camera.html', {
        'life': life,
        'camera_catalogs': camera_catalogs,
    })

@login_required
def incamera_film_unload(request, life_id):
    life = get_object_or_404(Life, pk=life_id)
    if not life.loaded:
        raise

    incamera = life.loaded
    incamera.unload(life.film_catalog.poses)
    life.unload()

    incamera.save()
    life.save()

    return render_to_response('incamera/unloaded.html', {
        'incamera': incamera,
    })

@login_required
def incamera_load(request, camera_catalog_id, film_catalog_id=None, life_id=None):
    camera_catalog = get_object_or_404(CameraCatalog, pk=camera_catalog_id)
    if film_catalog_id:
        film_catalog = get_object_or_404(Catalog, pk=film_catalog_id)
        if not film_catalog.remaining:
            raise

        life = film_catalog.remaining[0]
    elif life_id:
        life = get_object_or_404(Life, pk=life_id)
    else:
        raise

    incamera = InCamera(film_life=life, camera_catalog=camera_catalog)
    incamera.load()
    incamera.film_life.load()

    incamera.save()
    incamera.film_life.save()

    return render_to_response('incamera/loaded.html', {
        'incamera': incamera,
    })

@login_required
def incamera_develop(request, life_id):
    life = get_object_or_404(Life, pk=life_id)
    contacts = Developer.objects.all()
    return render_to_response('incamera/develop.html',
        context_instance=RequestContext(request, {
            'life': life,
            'contacts': contacts,
    }))


@login_required
@csrf_protect
def incamera_developed(request): #, life_id, contact_id):
    life_id = request.POST.get('life_id')
    contact_id = request.POST.get('contact_id')

    life = get_object_or_404(Life, pk=life_id)
    contact = get_object_or_404(Developer, pk=contact_id)
    life.devel(contact)
    life.save()
    return render_to_response('incamera/developed.html',
        context_instance=RequestContext(request, {
            'life': life,
            'contact': contact,
    }))

def incamera(request):
    incamera = list(InCamera.objects.all())
    incamera.sort(lambda a,b: cmp(a.film_life.reference, b.film_life.reference))
    return render_to_response('incamera/list.html', {
        'incamera': incamera,
    })

