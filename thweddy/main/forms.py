from django import forms
from django.forms.models import modelformset_factory

from thweddy.main.models import *

TweetFormSet = modelformset_factory(Tweet)

class ThreadForm(forms.ModelForm):
    username = forms.CharField(required=False)
    tweets = forms.ModelMultipleChoiceField(queryset=Tweet.objects.all(), required=False)
    _user = None
    _tweets = None
    class Meta:
        model = Thread

    def __init__(self, *args, **kwargs):
        user = kwargs.get('user', False)
        if not user is False:
            del kwargs['user']
        tweets = kwargs.get('tweets', False)
        if not tweets is False:
            del kwargs['tweets']
        super(forms.ModelForm, self).__init__(*args, **kwargs)
        self._user = user
        self._tweets = tweets

    def save(self, force_insert=False, force_update=False, commit=True):
        instance = super(forms.ModelForm, self).save(commit=False)
        instance.user = self._user
        instance.tweets = self._tweets
        instance.save()
        return instance

