from django.db import models
from django.contrib import admin
import tweepy

from thweddy.main.utils import get_anon_api


class TwitterUser(models.Model):
    username = models.CharField(max_length=140)


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    sort = models.IntegerField()
    class Meta:
        ordering = ('sort',)

    def original(self):
        return get_anon_api().get_status(self.tweet_id)


class Thread(models.Model):
    user = models.ForeignKey('TwitterUser')
    tweets = models.ManyToManyField('Tweet')



admin.site.register(TwitterUser)
admin.site.register(Tweet)
admin.site.register(Thread)
