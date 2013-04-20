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
    slug = models.CharField(max_length=255)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.title


class Feed(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User)
    tags = models.ManyToManyField(Tag, verbose_name="tags", related_name="feeds", blank=True)

    def __unicode__(self):
        return self.url


class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=255)
    date = models.DateField()
    summary = models.TextField()
    link = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    shortDescr = models.TextField()
    isRead = models.BooleanField()

    def __unicode__(self):
        return self.title
