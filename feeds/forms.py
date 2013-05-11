from django import forms
from feeds.models import *
from django.forms.formsets import formset_factory


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag


class ImportForm(forms.Form):
    removeOld = forms.BooleanField(label="Remove Old", required=False)
    file = forms.FileField()

FeedFormSet = formset_factory(FeedForm)
TagFormSet = formset_factory(TagForm)
