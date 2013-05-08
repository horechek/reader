# -*- coding: utf-8 -*-
import os
import opml

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import simplejson
from django.http import HttpResponse

from feeds.forms import *
from feeds.models import *
from feeds.tasks import update_feeds, update_new_feed, add_item_to_feed

from reader import settings


@login_required
def add_feed(request):
    if request.method == "POST":
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        form = FeedForm(post_values, initial={'user': request.user.id})
        if form.is_valid():
            feed = form.save()
            update_new_feed(feed)
            add_item_to_feed(feed)
            return redirect('/')
    else:
        form = FeedForm()
    return render(request, 'feeds/add_feed.html', {'form': form})


@login_required
def edit_feed(request, feed_id):
    pass


@login_required
def remove_feed(request, feed_id):
    Feed.objects.get(id=feed_id, user=request.user.id).delete()
    request.flash['info'] = 'Unsubscribed ok'
    return redirect('/')


@login_required
def add_tag(request):
    if request.method == "POST":
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        form = TagForm(post_values, initial={'user': request.user.id})
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TagForm()
    return render(request, 'feeds/add_tag.html', {'form': form})


@login_required
def edit_tag(request, tag_id):
    pass


@login_required
def remove_tag(request, tag_id):
    pass


@login_required
def settings_feeds(request):
    tags = Tag.objects.filter(user=request.user.id)
    feeds = Feed.objects.filter(user=request.user.id, tags__isnull=True)
    return render(request, 'feeds/settings.html', {'tags': tags, 'feeds': feeds})


@login_required
def import_feeds(request):
    if request.method == 'POST':
        form = ImportForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(
                request.FILES['file'],
                request.user,
                form.cleaned_data['removeOld'])
            return redirect('/')
    else:
        form = ImportForm()
    return render(request, 'feeds/import_feeds.html', {'form': form})


@login_required
def toggle_tag(request, tag_id):
    success = True
    try:
        tag = Tag.objects.get(pk=tag_id, user=request.user.id)
    except Tag.DoesNotExist:
        success = False

    tag.isOpen = not tag.isOpen
    tag.save()
    return HttpResponse(simplejson.dumps({'success': success, 'isOpen': tag.isOpen}),
                        mimetype='application/json')


@login_required
def main(request):
    tags = Tag.objects.filter(user=request.user.id)
    feeds = Feed.objects.filter(user=request.user.id, tags__isnull=True)
    all_notread_count = FeedItem.objects.filter(feed__user=request.user.id, isRead=0).count()
    return render(request, 'feeds/main.html',
                  {'feeds': feeds, 'tags': tags,
                  'all_notread_count': all_notread_count})


def load_items(request, feed_id=False, tag_id=False):

    items = FeedItem.objects.filter(feed__user=request.user.id)
    if feed_id:
        items = items.filter(feed=feed_id)
    elif tag_id:
        items = items.filter(feed__tags=tag_id)

    profile = request.user.get_profile()
    if profile.showUnread:
        items = items.exclude(isRead=1)
    items = items.order_by('date').reverse()
    json = toJSON(items)
    return HttpResponse(json, mimetype='application/json')


def load_item_content(request, item_id):
    item = FeedItem.objects.get(pk=item_id)
    item.isRead = True
    item.save()
    # if item.content:
    #     content = item.content
    # else:
    content = item.summary
    return HttpResponse(simplejson.dumps({'content': content,
                                          'title': "<a href='"+item.link+"' target='_blank'>"+item.title+"</a>",
                                          'date': item.date.strftime("%Y-%m-%d"),
                                          'isRead': item.isRead,
                                          'feedId': item.feed_id,
                                          'unreadCount': item.feed.get_unred_count()}),
                        mimetype='application/json')


def make_unread(request, item_id):
    item = FeedItem.objects.get(pk=item_id)
    item.isRead = False
    item.save()
    return HttpResponse(simplejson.dumps({'isRead': item.isRead,
                                          'feedId': item.feed_id,
                                          'unreadCount': item.feed.get_unred_count()}),
                        mimetype='application/json')


def get_unread_count(request):
    all_notread_count = FeedItem.objects.filter(feed__user=request.user.id, isRead=0).count()
    return HttpResponse(simplejson.dumps({'count': all_notread_count}),
                        mimetype='application/json')


def toJSON(obj):
    if isinstance(obj, QuerySet):
        return simplejson.dumps(obj, cls=DjangoJSONEncoder)
    if isinstance(obj, models.Model):
        set_obj = [obj]
        set_str = simplejson.dumps(simplejson.loads(serialize('json', set_obj)))
        str_obj = set_str[1:len(set_str)-2]
    return str_obj


def handle_uploaded_file(f, user, remove_old=True):
    remove_old = True
    directory = settings.MEDIA_ROOT + '/' + str(user.id) + '/'
    if remove_old:
        FeedItem.objects.filter(feed__user=user.id).delete()
        Tag.objects.filter(user=user.id).delete()
        Feed.objects.filter(user=user.id).delete()
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(directory + 'subscriptions.xml', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    outline = opml.parse(directory + 'subscriptions.xml')
    for item in outline:
        if len(item) > 1:
            tag = insert_tag(item, user)
            for parsefeed in item:
                insert_feed(parsefeed, user, tag)
        else:
            parsefeed = item
            insert_feed(parsefeed, user)
    update_feeds.delay(user)


def insert_feed(parsefeed, user, tag=False):
    try:
        try:
            feed = Feed.objects.get(url=parsefeed.xmlUrl)
        except Exception, e:
            feed = Feed()
        feed.url = parsefeed.xmlUrl
        feed.title = parsefeed.text
        feed.user = user
        feed.save()
        if tag:
            feed.tags.add(tag)
        feed.save()
    except Exception, e:
        pass


def insert_tag(parsetag, user):
    try:
        tag = Tag()
        tag.title = parsetag.text
        tag.user = user
        tag.save()
        return tag
    except Exception, e:
        return False
