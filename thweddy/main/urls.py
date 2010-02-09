from django.conf.urls.defaults import *

urlpatterns = patterns('thweddy.main',
    (r'^$', 'views.home'),
    (r'^verify-auth$', 'views.verify_auth'),
    (r'^new$', 'views.new'),
)
