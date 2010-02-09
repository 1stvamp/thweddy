from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from thweddy.main.models import *
from thweddy.main.forms import *
from thweddy.main.utils import get_api, user_login


def home(request):
    form = TwitterUserForm()
    return render_to_response('main/home.html', {'form': form})

def verify_auth(request):
    request.session['twitter_auth_verify_token'] = request.GET.get('oauth_verifier')
    return redirect('thweddy.main.views.new')

def new(request):
    api = get_api(request)
    if not api:
        return user_login(request)

    return render_to_response('main/home.html', {})

