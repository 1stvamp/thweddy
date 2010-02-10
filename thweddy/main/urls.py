from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import patterns, url

from thweddy.main.views import *

urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'^verify-auth$', verify_auth, name='verify-auth'),
    url(r'^new$', new_thread, name='new-thread'),
    url(r'^thread/(?P<id>\d+)$', cache_page(view_thread, 60 * 30), name='view-thread'),
)
