from django.db import models
from django.contrib import admin
import tweepy

from thweddy.main.twitter.settings import *


class TwitterUser(models.Model):
    username = models.CharField(max_length=140)


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    sort = models.IntegerField()
    class Meta:
        ordering = ('sort',)

    def original(self):
        return _get_api().get_status(self.tweet_id)


class Thread(models.Model):
    user = models.ForeignKey('TwitterUser')
    tweets = models.ManyToManyField('Tweet')


def _get_api():
    auth = tweepy.BasicAuthHandler(ANON_USER, ANON_PASS)
    return tweepy.API(auth)


admin.site.register(TwitterUser)
admin.site.register(Tweet)
admin.site.register(Thread)
