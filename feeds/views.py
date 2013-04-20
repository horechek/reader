# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import simplejson
from django .http import HttpResponse

from feeds.forms import *
from feeds.models import *


@login_required
def add_feed(request):
    if request.method == "POST":
        # data = request.POST
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        # print data
        form = FeedForm(post_values, initial={'user': request.user.id})
        # form.user = request.user.id
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = FeedForm()
    return render(request, 'feeds/add_feed.html', {'form': form})


@login_required
def add_tag(request):
    if request.method == "POST":
        # data = request.POST
        post_values = request.POST.copy()
        post_values['user'] = request.user.id
        # print data
        form = TagForm(post_values, initial={'user': request.user.id})
        # form.user = request.user.id
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = TagForm()
    return render(request, 'feeds/add_tag.html', {'form': form})


@login_required
def remove_feed(request, id):
    pass


@login_required
def import_feeds(request, id):
    pass


@login_required
def main(request):
    form = FeedForm()
    tagform = TagForm()
    tags = Tag.objects.filter(user=request.user.id)
    feeds = Feed.objects.filter(user=request.user.id, tags__isnull=True)
    return render(request, 'feeds/main.html',
                  {'feeds': feeds, 'tags': tags, 'form': form, 'tagform': tagform})


def load_items(request, feed_id=False, tag_id=False):
    if feed_id:
        items = FeedItem.objects.filter(feed=feed_id).order_by('date').reverse()
    elif tag_id:
        items = FeedItem.objects.filter(feed__user=request.user.id, feed__tags=tag_id).order_by('date').reverse()
    else:
        items = FeedItem.objects.filter(feed__user=request.user.id).order_by('date').reverse()
    json = toJSON(items)
    return HttpResponse(json, mimetype='application/json')


def load_item_content(request, item_id):
    item = FeedItem.objects.get(pk=item_id)
    item.isRead = True
    item.save()
    # json = toJSON(item)
    return HttpResponse(simplejson.dumps({'content': item.summary,
                                          'title': "<a href='"+item.link+"' target='_blank'>"+item.title+"</a>",
                                          'date': item.date.strftime("%Y-%m-%d"),
                                          'isRead': item.isRead}),
                        mimetype='application/json')


def set_item_read(request):
    pass


def toJSON(obj):
    if isinstance(obj, QuerySet):
        return simplejson.dumps(obj, cls=DjangoJSONEncoder)
    if isinstance(obj, models.Model):
        #do the same as above by making it a queryset first
        set_obj = [obj]
        set_str = simplejson.dumps(simplejson.loads(serialize('json', set_obj)))
        #eliminate brackets in the beginning and the end
        str_obj = set_str[1:len(set_str)-2]
    return str_obj
