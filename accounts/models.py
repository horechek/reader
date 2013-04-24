from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.ForeignKey(User, unique=True, related_name='profile')
    showUnread = models.BooleanField()

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])
models.signals.post_save.connect(create_profile, sender=User)
