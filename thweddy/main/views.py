from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect

from thweddy.main.models import *
from thweddy.main.forms import *


def home(request):
    form = TwitterUserForm()
    return render_to_response('main/home.html', {'form': form})

