from django import forms
from feeds.models import *


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag


class ImportForm(forms.Form):
    removeOld = forms.BooleanField(label="Remove Old", required=False)
    file = forms.FileField()
