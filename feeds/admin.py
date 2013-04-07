from feeds.models import *
from django.contrib import admin

class FeedAdmin(admin.ModelAdmin):
    pass

class FeedItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)