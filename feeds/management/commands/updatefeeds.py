# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.utils.html import strip_tags

import feedparser
from datetime import date

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
#
# http://wiki.python.org/moin/RssLibraries

class Command(BaseCommand):
    def handle(self, *args, **options):
        for feed in Feed.objects.all():
            f = feedparser.parse(feed.url)
            feed.title = f['channel']['title']
            if 'description' in f['channel']:
                feed.description = f['channel']['description']
            feed.link = f['channel']['link']
            feed.save()
            print feed.title
            for item in f['items']:
                try:
                    article = FeedItem.objects.get(link=item['link'])
                except:
                    article = FeedItem()
                article.link = item['link']
                article.title = item['title']
                # if 'date' in item:
                #     article.date = item['date']
                # else:
                d = date.today()
                article.date = d.strftime("%Y-%m-%d")
                if 'content' in item:
                    article.content = item['content']
                if 'summary' in item:
                    article.summary = item['summary']
                article.feed_id = feed.id
                article.shortDescr = strip_tags(article.summary)[0:25]
                article.save()
