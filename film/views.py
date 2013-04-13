from django.template import Context, loader, RequestContext
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from catalog2.film.models import Catalog, Life, InCamera, Sensitivity
from catalog2.camera.models import Catalog as CameraCatalog
from catalog2.contact.models import Developer
from catalog2.develop.models import Product
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
        'products': life.products.all(),
        'filmsheet': life.filmsheet,
    })

@login_required
def incamera_camera_load(request, camera_catalog_id):
    camera_catalog = get_object_or_404(CameraCatalog, pk=camera_catalog_id)
    film_catalogs = set()
    for film_format in camera_catalog.camera_model.possible_film_format.all():
        film_catalogs.update(film_format.catalog_set.all())

    return render_to_response('incamera/load_film.html', {
        'camera_catalog': camera_catalog,
        'film_catalogs': list(film_catalogs),
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
    camera_catalogs = CameraCatalog.objects.filter(sell_date=None)
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
            'products': Product.objects.filter(done=False),
            'product_len': Product.objects.filter(done=False).count(),
            'sensitivities': Sensitivity.objects.all(),
    }))


@login_required
@csrf_protect
def incamera_developed(request):
    life_id = request.POST.get('life_id')
    contact_id = request.POST.get('contact_id')
    products = request.POST.getlist('product')
    dev_iso = request.POST.get('dev_iso')

    life = get_object_or_404(Life, pk=life_id)
    contact = get_object_or_404(Developer, pk=contact_id)
    iso = get_object_or_404(Sensitivity, iso=dev_iso)
    for pid in products:
        product = get_object_or_404(Product, pk=pid)
        product.film_life.add(life)
        product.save()

    life.devel(contact, iso)
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

@login_required
def undo_last_life_load(request, life_id=None):
    if life_id:
        life = get_object_or_404(Life, pk=life_id)
        life.reinit()
        life.save()
        return render_to_response('film/actions.html')
    else:
        life = Life.last_inserted()
        if not life:
            return render_to_response('film/actions.html')

        return render_to_response('incamera/undo_last_life_load.html', {
            'life': life,
            'incamera': life.incamera.get().camera_catalog,
        })
