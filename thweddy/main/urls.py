from django.views.generic.simple import direct_to_template
from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import patterns, url

from thweddy.main.views import *

urlpatterns = patterns('',
    url(r'^$', direct_to_template, {'template': 'main/home.html'}, name='home'),
    url(r'^verify-auth$', verify_auth, name='verify-auth'),
    url(r'^new$', new_thread, name='new-thread'),
    url(r'^thread/(?P<id>\d+)$', cache_page(view_thread, 60 * 30), name='view-thread'),
    url(r'^latest$', cache_page(latest_threads, 60 * 15), name='latest-threads'),
    url(r'^mine$', user_threads, name='user-threads'),
    url(r'^ajax/lookup-thread$', ajax_lookup_thread, name='ajax-lookup-thread'),
    url(r'^faq$', direct_to_template, {'template': 'main/faq.html'}, name='faq'),
)
