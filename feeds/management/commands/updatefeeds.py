# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils.html import strip_tags
from django.contrib.auth.models import User

import feedparser
from time import mktime
from datetime import date, datetime

from feeds.models import *

import re

# _my_date_pattern = re.compile(
#     r'(\d{,2})/(\d{,2})/(\d{4}) (\d{,2}):(\d{2}):(\d{2})')

# def myDateHandler(aDateString):
#     """parse a UTC date in MM/DD/YYYY HH:MM:SS format"""
#     month, day, year, hour, minute, second = \
#         _my_date_pattern.search(aDateString).groups()
#     return (int(year), int(month), int(day), \
#         int(hour), int(minute), int(second), 0, 0, 0)

# feedparser.registerDateHandler(myDateHandler)
# http://wiki.python.org/moin/RssLibraries


class Command(BaseCommand):
    def handle(self, *args, **options):
        for user in User.objects.all():
            update_feeds_by_user(user)


def update_feeds_by_user(user):
    for feed in Feed.objects.filter(user=user):
        rss_feed = feedparser.parse(feed.url)
        feed = set_new_data_in_feed(feed, rss_feed)
        print feed.title + ":" + feed.url
        if 'items' in rss_feed:
            for rss_item in rss_feed['items']:
                set_new_data_in_feed_item(feed, rss_item)


def set_new_data_in_feed(feed, rss_feed):
    if 'title' in rss_feed['channel']:
        feed.title = rss_feed['channel']['title']
    else:
        feed.title = feed.url
    if 'description' in rss_feed['channel']:
        feed.description = rss_feed['channel']['description']
    if 'link' in rss_feed['channel']:
        feed.link = rss_feed['channel']['link']
    else:
        feed.link = feed.url
    feed.save()
    return feed


def set_new_data_in_feed_item(feed, rss_item):
    try:
        article = FeedItem.objects.get(link=rss_item['link'])
        update = True
    except:
        article = FeedItem()
        update = False

    if update:
        return
    try:
            # print rss_item
        if 'link' in rss_item:
            # print 'rss_item link: ' + rss_item['link']
            article.link = rss_item['link']
        if 'title' in rss_item:
            article.title = rss_item['title']
        else:
            article.title = rss_item['link']
        if 'date_parsed' in rss_item:
            d = datetime.fromtimestamp(mktime(rss_item['date_parsed']))
            article.date = d.strftime("%Y-%m-%d")
        elif 'published_parsed' in rss_item:
            d = datetime.fromtimestamp(mktime(rss_item['published_parsed']))
            article.date = d.strftime("%Y-%m-%d")
            # article.date = rss_item['date']
        elif not update:
            d = date.today()
            article.date = d.strftime("%Y-%m-%d")

        print article.date

        if 'content' in rss_item:
            article.content = rss_item['content']
        if 'summary' in rss_item:
            article.summary = rss_item['summary']
            # if 'date' in rss_item['summary']:
            #     print rss_item['summary']['date']
        article.feed_id = feed.id
        article.shortDescr = strip_tags(article.summary)[0:45] + '...'
        article.save()
    except Exception, e:
        pass
