from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from reader import settings

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'feeds.views.main', name='home'),
    # url(r'^reader/', include('reader.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^register/$', 'reader.views.register', name='register'),
    url(r'^login/$', 'reader.views.login', name='login'),
    url(r'^logout/$', 'reader.views.logout', name='logout'),
    url(r'^feeds/', include('feeds.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
)
