import tweepy
from django.shortcuts import redirect

from thweddy.main.twitter.settings import *

def user_login():
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # Redirect user to Twitter to authorize
    return redirect(auth.get_authorization_url())


def get_api(verify_token):
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

    # Get access token
    auth.get_access_token(verify_token)

    # API instance
    return tweepy.API(auth)

