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


    # cameras
    url(r'^camera/?$', 'camera.views.list'),
    url(r'^camera/(?P<catalog_id>\d+)/?$', 'camera.views.info'),
    url(r'^camera/(?P<catalog_id>\d+)/edit/?$', 'camera.views.edit'),
    url(r'^camera/(?P<catalog_id>\d+)/update/?$', 'camera.views.update'),
)
