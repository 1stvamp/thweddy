from django.db import models
import tweepy

from thweddy.main.twitter.utils import get_anon_api


class TwitterUser(models.Model):
    username = models.CharField(max_length=140)

    def __unicode__(self):
        return u'TwitterUser (%s)' % (self.username,)


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    sort = models.IntegerField(blank=False, null=True, default=0)
    _original = None
    _api = None

    class Meta:
        ordering = ('sort', 'id',)

    def __unicode__(self):
        return u'Tweet %s' % (self.tweet_id,)

    @property
    def original(self):
        if not  self._original:
            try:
                if self._api:
                    api = self._api
                else:
                    api = get_anon_api()
                self._original = api.get_status(self.tweet_id)
            except tweepy.TweepError:
                pass
        return self._original


class Thread(models.Model):
    user = models.ForeignKey('TwitterUser')
    tweets = models.ManyToManyField('Tweet')

    def __unicode__(self):
        return u'Thread "%s" by %s' % (
            ', '.join(t.tweet_id for t in self.tweets.all()),
            self.user.username,
        )


