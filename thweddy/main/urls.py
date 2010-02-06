from django.conf.urls.defaults import *

urlpatterns = patterns('thweddy.main',
    (r'^$', 'views.home'),
)
