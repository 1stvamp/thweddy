import re
import tweepy
from django.shortcuts import redirect

from thweddy.main.twitter.settings import *

def _auth():
    return tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET, CALLBACK_URL)

def user_login(request):
    auth = _auth()

    redirect_url = auth.get_authorization_url()

    request.session['twitter_auth_request_token'] = (auth.request_token.key, auth.request_token.secret,)

    # Redirect user to Twitter to authorize
    return redirect(redirect_url)


def get_api(request):
    auth = _auth()


    # Get access token
    access_token = request.session.get('twitter_auth_access_token', None)

    if not access_token:
        verify_token = request.session.get('twitter_auth_verify_token', None)
        request_token = request.session.get('twitter_auth_request_token', None)

        if not verify_token or not request_token:
            return False

        auth.set_request_token(request_token[0], request_token[1])

        try:
            auth.get_access_token(verify_token)
        except tweepy.TweepError:
            return False

        request.session['twitter_auth_access_token'] = (auth.access_token.key, auth.access_token.secret,)
    else:
        auth.set_access_token(access_token[0], access_token[1])

    # API instance
    return tweepy.API(auth)


def get_anon_api():
    auth = tweepy.BasicAuthHandler(ANON_USER, ANON_PASS)
    return tweepy.API(auth)


def parse_tweet_id(id):
    tweet_id = None
    if 'status' in id:
        m = re.search(r'/status/(\d+)', id)
        if m and m.group(1):
            tweet_id = m.group(1)
    return tweet_id

