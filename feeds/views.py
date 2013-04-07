# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def add_feed(request):
    return render(request, 'feeds/add.html')

def remove_feed(request, id):
    pass