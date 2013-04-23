from django.db import models
from django.contrib.auth.models import User

from django.core.serializers import serialize
from django.utils.simplejson import dumps, loads, JSONEncoder
from django.db.models.query import QuerySet
from django.utils.functional import curry


class DjangoJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, QuerySet):
            # `default` must return a python serializable
            # structure, the easiest way is to load the JSON
            # string produced by `serialize` and return it
            return loads(serialize('json', obj))
        return JSONEncoder.default(self, obj)


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User)
    isOpen = models.BooleanField()

    def __unicode__(self):
        return self.title

    def get_unred_count(self):
        return FeedItem.objects.filter(feed__tags=self.id, isRead=0).count()


class Feed(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, verbose_name="tags", related_name="feeds", blank=True)

    def __unicode__(self):
        return self.url

    def get_unred_count(self):
        return FeedItem.objects.filter(feed=self.id, isRead=0).count()


class FeedItem(models.Model):
    feed = models.ForeignKey(Feed, related_name="items")
    title = models.CharField(max_length=255)
    date = models.DateField()
    summary = models.TextField()
    link = models.TextField()
    content = models.TextField(blank=True)
    shortDescr = models.TextField()
    isRead = models.BooleanField()

    def __unicode__(self):
        return self.title
