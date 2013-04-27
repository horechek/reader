from celery.decorators import task, periodic_task
from celery.task.schedules import crontab
from django.contrib.auth.models import User

from feeds.management.commands.updatefeeds import update_feeds_by_user


@task
def update_feed(user):
    update_feeds_by_user(user)


# @periodic_task(run_every=crontab(hour=0, minute=30))
@task
def update_all_feeds():
    for user in User.objects.all():
            update_feeds_by_user(user)
