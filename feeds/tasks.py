from celery.decorators import task, periodic_task
from celery.task.schedules import crontab
from django.contrib.auth.models import User
import feedparser

from feeds.management.commands.updatefeeds import update_feeds_by_user, set_new_data_in_feed, add_new_item_to_feed


@task()
def update_feeds(user):
    update_feeds_by_user(user)


@task()
def update_new_feed(feed):
    rss_feed = feedparser.parse(feed.url)
    set_new_data_in_feed(feed, rss_feed)


@task()
def add_item_to_feed(feed):
    rss_feed = feedparser.parse(feed.url)
    add_new_item_to_feed(feed, rss_feed)


# @periodic_task(run_every=crontab(hour=0, minute=30))
@task()
def update_all_feeds():
    for user in User.objects.all():
            update_feeds_by_user(user)
