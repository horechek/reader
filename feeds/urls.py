from django.conf.urls import url, patterns, include

urlpatterns = patterns('feeds.views',
    url(r'add/$', 'add_feed', name='add_feed'),
    url(r'edit/(?P<feed_id>[\d]*)/$', 'edit_feed', name='edit_feed'),
    url(r'remove/(?P<feed_id>[\d]*)/$', 'remove_feed', name='remove_feed'),

    url(r'add_tag/$', 'add_tag', name='add_tag'),
    url(r'edit_tag/(?P<tag_id>[\d]*)/$', 'edit_tag', name='edit_tag'),
    url(r'remove_tag/(?P<tag_id>[\d]*)/$', 'remove_tag', name='remove_tag'),
    url(r'toggle_tag/(?P<tag_id>[\d]*)/$', 'toggle_tag', name='toggle_tag'),

    url(r'load_items/feed/(?P<feed_id>[\d]*)/$', 'load_items', name='load_items'),
    url(r'load_items/tag/(?P<tag_id>[\d]*)/$', 'load_items', name='load_items_tag'),
    url(r'load_items/$', 'load_items', name='load_items_all'),

    url(r'load_item_content/(?P<item_id>[\d]*)/$', 'load_item_content', name='load_item_content'),
    url(r'make_unread/(?P<item_id>[\d]*)/$', 'make_unread', name='make_unread'),
    url(r'get_unread_count/$', 'get_unread_count', name='get_unread_count'),

    url(r'import/$', 'import_feeds', name='import_feeds'),
    url(r'settings/$', 'settings_feeds', name='settings_feeds'),
)
