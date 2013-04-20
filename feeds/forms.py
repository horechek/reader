from django import forms
from feeds.models import *


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
