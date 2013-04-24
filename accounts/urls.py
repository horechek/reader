from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^set_show/(?P<show_unread>[\d]*)/$', 'set_show', name='set_show'),
)