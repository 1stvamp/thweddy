from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect, get_object_or_404

from thweddy.main.models import *
from thweddy.main.forms import *
from thweddy.main.utils import get_api, user_login


def home(request):
    return render_to_response('main/home.html', {})

def verify_auth(request):
    request.session['twitter_auth_verify_token'] = request.GET.get('oauth_verifier')
    return redirect('thweddy.main.views.new_thread')

def new_thread(request):
    api = get_api(request)
    if not api:
        return user_login(request)

    user = request.session.get('twitter_user', None)
    if not user:
        user = TwitterUser.objects.get_or_create(username=api.me().screen_name)
        request.session['twitter_user'] = user

    if request.method == 'POST':
        form = ThreadForm(request.POST, user=user)
        if form.is_valid():
            form.save()
    else:
        form = ThreadForm(user=user)
        formset = TweetFormSet(queryset=Tweet.objects.none())

    return render_to_response(
        'main/new.html',
        {
            'form': form,
            'formset': formset,
        }
    )

def view_thread(request, id):
    thread = get_object_or_404(Thread, pk=id)
    return HttpResponse('')


