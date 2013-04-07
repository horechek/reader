from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=255)
    slug = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title

class Feed(models.Model):
    url = models.CharField(max_length = 255)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=255, blank=True)
    link = models.CharField(max_length=255, blank=True)
    user = models.OneToOneField(User)
    tags = models.ManyToManyField(Tag, verbose_name="tags", related_name="tags", blank=True)
    
    def __unicode__(self):
        return self.url

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=255)
    date = models.DateField()
    summary = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    content = models.TextField()
    
    def __unicode__(self):
        return self.title
