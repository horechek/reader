from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Feed(models.Model):
    url = models.CharField(max_length = 255)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    link = models.CharField(max_length=255)
    user = models.OneToOneField(User)
    
    def __unicode__(self):
        return self.title

class FeedItem(models.Model):
    feed = models.ForeignKey(Feed)
    title = models.CharField(max_length=255)
    date = models.DateField()
    summary = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    content = models.TextField()
    
    def __unicode__(self):
        return self.title
