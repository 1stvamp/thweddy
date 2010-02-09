from django.views.decorators.cache import cache_page
from django.conf.urls.defaults import patterns

from thweddy.main.views import *

urlpatterns = patterns('',
    (r'^$', home),
    (r'^verify-auth$', verify_auth),
    (r'^new$', new_thread),
    (r'^thread/(?P<id>\d+)$', cache_page(view_thread, 60 * 30)),
)
