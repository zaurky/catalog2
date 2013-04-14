from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # admin
    url(r'^admin/', include(admin.site.urls)),

    # login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # index
    url(r'^/?$', 'django.views.generic.simple.direct_to_template', {
        'template': 'index.html'}),

    # other
    url(r'stats', 'catalog2.other.views.stats'),

    # cameras
    url(r'^/?$', 'catalog2.camera.views.catalog_list'),
    url(r'^camera/catalog/?$', 'catalog2.camera.views.catalog_list'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/?$',
        'catalog2.camera.views.catalog_info'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/edit/?$',
        'catalog2.camera.views.catalog_edit'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/update/?$',
        'catalog2.camera.views.catalog_update'),

    url(r'^camera/catalog/sell/(?P<catalog_id>\d+)/?$',
        'catalog2.camera.views.catalog_sell'),
    url(r'^camera/catalog/selling/?$',
        'catalog2.camera.views.catalog_selling'),
    url(r'^camera/catalog/sold/(?P<catalog_id>\d+)/?$',
        'catalog2.camera.views.catalog_sold'),

    # films
    url(r'^film/catalog/?$', 'catalog2.film.views.catalog_list'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/?$',
        'catalog2.film.views.catalog_info'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/edit/?$',
        'catalog2.film.views.catalog_edit'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/update/?$',
        'catalog2.film.views.catalog_update'),

    url(r'^film/life/(?P<life_id>\d+)/?$', 'catalog2.film.views.life_view'),

    url(r'^film/incamera/?$', 'catalog2.film.views.incamera'),
    url(r'^film/incamera/load/camera/(?P<camera_catalog_id>\d+)/?$',
        'catalog2.film.views.incamera_camera_load'),
    url(r'^film/incamera/load/life/(?P<life_id>\d+)/?$',
        'catalog2.film.views.incamera_film_load'),
    url(r'^film/incamera/load/(?P<camera_catalog_id>\d+)/camera/(?P<film_catalog_id>\d+)/?$',
        'catalog2.film.views.incamera_load'),
    url(r'^film/incamera/load/(?P<camera_catalog_id>\d+)/film/(?P<life_id>\d+)/?$',
        'catalog2.film.views.incamera_load'),
    url(r'^film/incamera/unload/camera/(?P<camera_catalog_id>\d+)/?$',
        'catalog2.film.views.incamera_camera_unload'),
    url(r'^film/incamera/unload/life/(?P<life_id>\d+)/?$',
        'catalog2.film.views.incamera_film_unload'),
    url(r'^film/incamera/develop/(?P<life_id>\d+)/?$',
        'catalog2.film.views.incamera_develop'),
    url(r'^film/incamera/developed/?$',
        'catalog2.film.views.incamera_developed'),

    url(r'^film/life/undo_load/?(?P<life_id>\d+)?/?$',
        'catalog2.film.views.undo_last_life_load'),

    # film actions shortcut
    url(r'^film/action/?', 'django.views.generic.simple.direct_to_template', {
        'template': 'film/actions.html'}),

    # media
    url(r'^media/?$', 'catalog2.media.views.media_list'),
    url(r'^media/media/(?P<media_id>\d+)/?$',
        'catalog2.media.views.media_info'),
    url(r'^media/link/camera/(?P<media_id>\d+)/?$',
        'catalog2.media.views.media_link_camera'),
    url(r'^media/link/exemple/(?P<media_id>\d+)/?$',
        'catalog2.media.views.media_link_exemple'),
    url(r'^media/link/filmsheet/(?P<media_id>\d+)/?$',
        'catalog2.media.views.media_link_filmsheet'),
    url(r'^media/link/camera/(?P<media_id>\d+)/(?P<catalog_id>\d+)/?$',
        'catalog2.media.views.media_linked_camera'),
    url(r'^media/link/exemple/(?P<media_id>\d+)/(?P<life_id>\d+)/?$',
        'catalog2.media.views.media_linked_exemple'),
    url(r'^media/link/filmsheet/(?P<media_id>\d+)/(?P<life_id>\d+)/?$',
        'catalog2.media.views.media_linked_filmsheet'),
    url(r'^media/upload/?$', 'catalog2.media.views.upload'),
    url(r'^media/do_upload/?$', 'catalog2.media.views.do_upload'),
    url(r'^media/tag/add/(?P<media_id>\d+)(/(?P<tag_id>\d+))?/?$',
        'catalog2.media.views.add_tag'),
    url(r'^media/display/(?P<media_id>\d+)/?$',
        'catalog2.media.views.display'),

    # lens
    url(r'^lens/catalog/?$', 'catalog2.lens.views.catalog_list'),
    url(r'^lens/catalog/(?P<lens_id>\d+)/?$', 'catalog2.lens.views.catalog_info'),

    url(r'^lens/catalog/sell/(?P<catalog_id>\d+)/?$',
        'catalog2.lens.views.catalog_sell'),
    url(r'^lens/catalog/selling/?$',
        'catalog2.lens.views.catalog_selling'),
    url(r'^lens/catalog/sold/(?P<catalog_id>\d+)/?$',
        'catalog2.lens.views.catalog_sold'),
)
