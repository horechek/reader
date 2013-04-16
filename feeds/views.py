# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import simplejson
from django .http import HttpResponse

from feeds.forms import *
from feeds.models import *


@login_required
def add_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        feed = form.save()
    else:
        form = FeedForm()
    return render(request, 'feeds/add.html', {'form': form})


@login_required
def remove_feed(request, id):
    pass


@login_required
def main(request):
    feeds = Feed.objects.filter(user=request.user.id)
    return render(request, 'feeds/main.html', {'feeds': feeds})


def load_items(request, feed_id):
    items = FeedItem.objects.filter(feed=feed_id)
    json = toJSON(items)
    return HttpResponse(json, mimetype='application/json')


def load_item_content(request, item_id):
    item = FeedItem.objects.get(pk=item_id)
    # json = toJSON(item)
    return HttpResponse(simplejson.dumps({'content': item.summary,
                                          'title': item.title}),
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
