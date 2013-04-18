from django.conf.urls import url, patterns, include

urlpatterns = patterns('feeds.views',
    url(r'add/$', 'add_feed', name='add_feed'),
    url(r'load_items/(?P<feed_id>[\d]*)/$', 'load_items', name='load_items'),
    url(r'load_items/tag/(?P<tag_id>[\d]*)/$', 'load_items', name='load_items_tag'),
    url(r'load_items/$', 'load_items', name='load_items_all'),
    url(r'load_item_content/(?P<item_id>[\d]*)/$', 'load_item_content', name='load_item_content'),
)
