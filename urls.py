from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'catalog2.views.home', name='home'),
    # url(r'^catalog2/', include('catalog2.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # login
    url(r'^accounts/login/$', 'django.contrib.auth.views.login'),

    # cameras
    url(r'^/?$', 'camera.views.catalog_list'),
    url(r'^camera/catalog/?$', 'camera.views.catalog_list'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/?$', 'camera.views.catalog_info'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/edit/?$', 'camera.views.catalog_edit'),
    url(r'^camera/catalog/(?P<catalog_id>\d+)/update/?$',
    'camera.views.catalog_update'),

    # films
    url(r'^film/catalog/?$', 'film.views.catalog_list'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/?$', 'film.views.catalog_info'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/edit/?$', 'film.views.catalog_edit'),
    url(r'^film/catalog/(?P<catalog_id>\d+)/update/?$', 'film.views.catalog_update'),

    url(r'^film/life/(?P<life_id>\d+)/?$', 'film.views.life_view'),
)
