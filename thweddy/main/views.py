from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.views.decorators.cache import cache_control

from thweddy.main.models import *
from thweddy.main.forms import *
from thweddy.main.utils import get_api, user_login


def home(request):
    return render_to_response('main/home.html', {})

def verify_auth(request):
    request.session['twitter_auth_verify_token'] = request.GET.get('oauth_verifier')
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
            return redirect('view-thread', id=thread.id)
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


