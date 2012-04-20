from catalog2.media.models import *

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
    })
