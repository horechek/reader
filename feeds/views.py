# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

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
    pass

def load_item_content(request, item_id):
    pass

def set_item_read(request):
    pass
