from django.db import models
import tweepy

from thweddy.main.twitter.utils import get_anon_api


class TwitterUser(models.Model):
    username = models.CharField(max_length=140)

    def __unicode__(self):
        return u'TwitterUser (%s)' % (self.username,)


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    sort = models.IntegerField()
    _original = None

    class Meta:
        ordering = ('sort',)

    def __unicode__(self):
        return u'Tweet %s' % (self.tweet_id,)

    @property
    def original(self):
        if not  self._original:
            self._original = get_anon_api().get_status(self.tweet_id)
        return self._original


class Thread(models.Model):
    user = models.ForeignKey('TwitterUser')
    tweets = models.ManyToManyField('Tweet')

    def __unicode__(self):
        return u'Thread "%s" by %s' % (
            ', '.join(t.tweet_id for t in self.tweets.all()),
            self.user.username,
        )


