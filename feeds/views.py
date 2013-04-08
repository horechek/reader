# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from feeds.forms import *

@login_required
def add_feed(request):
    if request.method == "POST":
        form = FeedForm(request.POST)
        feed = form.save()
    else:
        form = FeedForm()
    return render(request, 'feeds/add.html', {'form': form})

def remove_feed(request, id):
    pass

def main(request):
    pass