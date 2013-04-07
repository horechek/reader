from django.conf.urls import url, patterns, include

urlpatterns = patterns('feeds.views',
    url(r'add/$', 'add_feed', name='add_feed'),
)
