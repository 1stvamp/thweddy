from django import forms
from django.forms.models import modelformset_factory
import re

from thweddy.main.models import *

class TweetForm(forms.ModelForm):
    tweet_id = forms.CharField(label=u'Tweet ID or URL')
    class Meta:
        model = Tweet

    def clean_tweet_id(self):
        tweet_id = self.cleaned_data.get('tweet_id', None)
        try:
            int(tweet_id)
        except:
            if 'status' in tweet_id:
                m = re.search(r'/status/(\d+)', tweet_id)
                if m and m.group(1):
                    tweet_id = m.group(1)
            else:
                raise forms.ValidationError('Invalid Tweet ID or Twitter status URL')
        return tweet_id

TweetFormSet = modelformset_factory(Tweet, form=TweetForm, fields=('tweet_id',), extra=1)

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

