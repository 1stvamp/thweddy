from django.http import HttpResponse, HttpRequest
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.core import urlresolvers

from thweddy.main.models import *
from thweddy.main.forms import *
from thweddy.main.twitter.utils import *
from thweddy.main.decorators import jsonify
from thweddy.main.utils import expire_page

from tweepy import TweepError


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
        r = user_login(request)
        if r:
            return r
        # Twitter fail, so display a nice message to the user
        return render_to_response(
            'main/failwhale.html',
            {'path': request.path,}
        )

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
                if t.sort == '':
                    t.sort = i
                t.save()
                thread.tweets.add(t)
                i += 1
            thread.save()
            # Invalidate my threads rendered template cache
            if request.session.has_key('my-threads-render'):
                del request.session['my-threads-render']
            return redirect('view-thread', id=thread.id)
    else:
        formset = TweetFormSet(queryset=Tweet.objects.none())

    return render_to_response(
        'main/new.html',
        {
            'formset': formset,
        }
    )


def edit_thread(request, id):
    thread = get_object_or_404(Thread, pk=id)

    api = get_api(request)
    if not api:
        r = user_login(request, reverse('edit-thread', kwargs={'id': id}))
        if r:
            return r
        # Twitter fail, so display a nice message to the user
        return render_to_response(
            'main/failwhale.html',
            {'path': request.path,}
        )

    user = request.session.get('twitter_user', None)
    if not user:
        user, user_created = TwitterUser.objects.get_or_create(username=api.me().screen_name)
        request.session['twitter_user'] = user

    # Check permissions to edit thread
    if user.id != thread.user.id:
        return HttpNotAllowedResponse('Naught, naughty, not your thread!')

    if request.method == 'POST':
        formset = TweetFormSet(request.POST, queryset=thread.tweets.all())
        if formset.is_valid():
            tweets = formset.save(commit=False)
            i = 0
            for t in tweets:
                if t.sort == '':
                    t.sort = i
                t.save()
                thread.tweets.add(t)
                i += 1
            thread.save()
            # Invalidate my threads rendered template cache
            if request.session.has_key('my-threads-render'):
                del request.session['my-threads-render']
            # Expire the in-memory cache of the view page
            expire_page(reverse('view-thread', kwargs={'id': thread.id,}))
            return redirect('view-thread', id=thread.id)
    else:
        formset = TweetFormSet(queryset=thread.tweets.all())

    return render_to_response(
        'main/edit.html',
        {
            'formset': formset,
        }
    )

def view_thread(request, id):
    thread = get_object_or_404(Thread, pk=id)

    user = request.session.get('twitter_user', None)
    return render_to_response('main/view.html', {'thread': thread, 'user': user,})


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
                r = user_login(request)
                if r:
                    return r
                # Twitter fail, so display a nice message to the user
                return render_to_response(
                    'main/failwhale.html',
                    {'path': request.path,}
                )

            try:
                user = TwitterUser.objects.get(username=api.me().screen_name)
                request.session['twitter_user'] = user
            except TwitterUser.DoesNotExist:
                user = None
        request.session['my-threads-render'] = render_to_response('main/mine.html', {'user': user,})
        return request.session['my-threads-render']


@jsonify
def ajax_lookup_thread(request):
    def _get_status(api, id):
        try:
            t = api.get_status(id)
        except TweepError:
            return None
        else:
            return t

    original_tweet_id = request.GET.get('tweet_id', None)
    try:
        tweet_id = int(original_tweet_id)
    except:
        tweet_id = parse_tweet_id(original_tweet_id)

    if not tweet_id:
        return {'error': 'No tweet matching "%s" found.' % (original_tweet_id),}

    api = get_api(request)
    if not api:
        api = get_anon_api(request)

    thread = []
    tweet = _get_status(api, tweet_id)
    if tweet:
        thread.append(tweet_id)
        if tweet.in_reply_to_status_id:
            t = _get_status(api, tweet.in_reply_to_status_id)
            while t:
                thread.append(t.id)
                if t.in_reply_to_status_id:
                    t = _get_status(api, t.in_reply_to_status_id)
                else:
                    t = False

        thread.reverse()

    if len(thread) <= 1:
        thread = {'error': 'No related tweets found.'}

    return thread

