from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from thweddy.main.models import *


def home(request):
    return render_to_response('main/home.html', {})

