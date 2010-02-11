from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core import urlresolvers

from thweddy.main.models import *
from thweddy.main.forms import *
from thweddy.main.utils import *
from thweddy.main.decorators import jsonify


def verify_auth(request):
    request.session['twitter_auth_verify_token'] = request.GET.get('oauth_verifier')
    return_url = request.session.get('twitter_auth_return_url', None)
    if return_url:
        return redirect(return_url)
    else:
        return redirect('new-thread')

def new_thread(request):
    api = get_api(request)
    if not api:
        return user_login(request)

    user = request.session.get('twitter_user', None)
    if not user:
        user, user_created = TwitterUser.objects.get_or_create(username=api.me().screen_name)
        request.session['twitter_user'] = user

    if request.method == 'POST':
        formset = TweetFormSet(request.POST)
        if formset.is_valid():
            thread = Thread.objects.create(user=user)
            tweets = formset.save(commit=False)
            i = 0
            for t in tweets:
                t.sort = i
                t.save()
                thread.tweets.add(t)
                i += 1
            thread.save()
            # Invalidate my threads rendered template cache
            if request.session.has_key('my-threads-render'):
                del request.session['my-threads-render']
            return redirect('view-thread', id=thread.id)
        elif not formset.errors[0]:
            print 'blah'
    else:
        formset = TweetFormSet(queryset=Tweet.objects.none())

    return render_to_response(
        'main/new.html',
        {
            'formset': formset,
        }
    )


def view_thread(request, id):
    thread = get_object_or_404(Thread, pk=id)
    return render_to_response('main/view.html', {'thread': thread,})


def latest_threads(request):
    threads = Thread.objects.all().order_by('-pk')[:20]
    return render_to_response('main/latest.html', {'threads': threads,})


def user_threads(request):
    rendered = request.session.get('my-threads-render', None)
    if rendered:
        return rendered
    else:
        user = request.session.get('twitter_user', None)
        if not user:
            api = get_api(request)
            if not api:
                request.session['twitter_auth_return_url'] = urlresolvers.reverse('user-threads')
                return user_login(request)

            user = get_object_or_404(TwitterUser, username=api.me().screen_name)
            request.session['twitter_user'] = user
        request.session['my-threads-render'] = render_to_response('main/mine.html', {'user': user,})
        return request.session['my-threads-render']


@jsonify
def ajax_lookup_thread(request):
    tweet_id = request.GET.get('tweet_id', None)
    try:
        int(tweet_id)
    except:
        tweet_id = parse_tweet_id(tweet_id)

    if not tweet_id:
        return ''

    api = get_api(request)
    if not api:
        api = get_anon_api(request)

    thread = [tweet_id]
    tweet = api.get_status(tweet_id)
    if tweet:
        if tweet.in_reply_to_status_id:
            t = api.get_status(tweet.in_reply_to_status_id)
            while t:
                thread.append(t.id)
                if t.in_reply_to_status_id:
                    t = api.get_status(t.in_reply_to_status_id)
                else:
                    t = False

    thread.reverse()
    return thread

