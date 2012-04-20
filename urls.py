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

    # cameras
    url(r'^/?$', 'camera.views.catalog_list'),
    url(r'^camera/catalog/?$', 'camera.views.catalog_list'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/?$', 'camera.views.catalog_info'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/edit/?$',
        'camera.views.catalog_edit'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/update/?$',
        'camera.views.catalog_update'),

    # films
    url(r'^film/catalog/?$', 'film.views.catalog_list'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/?$', 'film.views.catalog_info'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/edit/?$',
        'film.views.catalog_edit'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/update/?$',
        'film.views.catalog_update'),

    url(r'^film/life/(?P<life_id>\d+)/?$', 'film.views.life_view'),

    url(r'^film/incamera/?$', 'film.views.incamera'),
    url(r'^film/incamera/load/camera/(?P<camera_catalog_id>\d+)/?$',
        'film.views.incamera_camera_load'),
    url(r'^film/incamera/load/life/(?P<life_id>\d+)/?$',
        'film.views.incamera_film_load'),
    url(r'^film/incamera/load/(?P<camera_catalog_id>\d+)/camera/(?P<film_catalog_id>\d+)/?$',
        'film.views.incamera_load'),
    url(r'^film/incamera/load/(?P<camera_catalog_id>\d+)/film/(?P<life_id>\d+)/?$',
        'film.views.incamera_load'),
    url(r'^film/incamera/unload/camera/(?P<camera_catalog_id>\d+)/?$',
        'film.views.incamera_camera_unload'),
    url(r'^film/incamera/unload/life/(?P<life_id>\d+)/?$',
        'film.views.incamera_film_unload'),
    url(r'^film/incamera/develop/(?P<life_id>\d+)/?$',
        'film.views.incamera_develop'),
    url(r'^film/incamera/developed/?$', 'film.views.incamera_developed'),

    # media
    url(r'^media/?$', 'media.views.media_list'),
    url(r'^media/media/(?P<media_id>\d+)?$', 'media.views.media_info'),
)
