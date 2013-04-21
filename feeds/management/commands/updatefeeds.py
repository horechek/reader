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
            for feed in Feed.objects.filter(user=user):
                # feed = Feed.objects.get(pk=874)
                # # url = 'http://feeds.feedburner.com/AntonShevchuk'
                f = feedparser.parse(feed.url)
                if 'title' in f['channel']:
                    feed.title = f['channel']['title']
                else:
                    feed.title = feed.url
                if 'description' in f['channel']:
                    feed.description = f['channel']['description']
                if 'link' in f['channel']:
                    feed.link = f['channel']['link']
                else:
                    feed.link = feed.url
                feed.save()
                print feed.title + ":" + feed.url
                if 'items' in f:
                    for item in f['items']:
                        try:
                            article = FeedItem.objects.get(link=item['link'])
                            update = True
                        except:
                            article = FeedItem()
                            update = False

                        if update:
                            continue
                        try:
                                # print item
                            if 'link' in item:
                                # print 'item link: ' + item['link']
                                article.link = item['link']
                            if 'title' in item:
                                article.title = item['title']
                            else:
                                article.title = item['link']
                            if 'date_parsed' in item:
                                d = datetime.fromtimestamp(mktime(item['date_parsed']))
                                article.date = d.strftime("%Y-%m-%d")
                            elif 'published_parsed' in item:
                                d = datetime.fromtimestamp(mktime(item['published_parsed']))
                                article.date = d.strftime("%Y-%m-%d")
                                # article.date = item['date']
                            elif not update:
                                d = date.today()
                                article.date = d.strftime("%Y-%m-%d")

                            print article.date

                            if 'content' in item:
                                article.content = item['content']
                            if 'summary' in item:
                                article.summary = item['summary']
                                # if 'date' in item['summary']:
                                #     print item['summary']['date']
                            article.feed_id = feed.id
                            article.shortDescr = strip_tags(article.summary)[0:45] + '...'
                            article.save()
                        except Exception, e:
                            pass
