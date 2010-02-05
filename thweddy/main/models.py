from django.db import models
from django.contrib import admin


class TwitterUser(models.Model):
    username = models.CharField(max_length=140)


class Tweet(models.Model):
    tweet_id = models.CharField(max_length=255)
    sort = models.IntegerField()


class Thread(models.Model):
    user = models.ForeignKey('TwitterUser')
    tweets = models.ManyToManyField('Tweet')
    hash = models.CharField(max_length=255)


admin.site.register(TwitterUser)
admin.site.register(Tweet)
admin.site.register(Thread)
