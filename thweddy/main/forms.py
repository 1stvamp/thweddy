from django import forms
from django.forms.util import ErrorList
from django.forms.models import modelformset_factory

from thweddy.main.models import *
from thweddy.main.twitter.utils import *

class TweetForm(forms.ModelForm):
    tweet_id = forms.CharField(label=u'Tweet ID or URL')
    class Meta:
        model = Tweet

    def clean_tweet_id(self):
        tweet_id = self.cleaned_data.get('tweet_id', None)
        try:
            int(tweet_id)
        except:
            tweet_id = parse_tweet_id(tweet_id)
            if not tweet_id:
                raise forms.ValidationError('Invalid Tweet ID or URL')
        return tweet_id

class BaseTweetFormset(forms.models.BaseModelFormSet):
    def clean(self):
        super(BaseTweetFormset, self).clean()
        at_least_one = False
        for form in self.forms:
            if hasattr(form, 'cleaned_data') and form.cleaned_data:
                at_least_one = True
                break
        if not at_least_one and len(self.forms):
            self.forms[0]._errors['tweet_id'] = ErrorList(['Must have at least one tweet!'])
            raise forms.ValidationError('Must have at least one tweet!')

TweetFormSet = modelformset_factory(Tweet, form=TweetForm,
                                    formset=BaseTweetFormset,
                                    fields=('tweet_id',), extra=1)

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

