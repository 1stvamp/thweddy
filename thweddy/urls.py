from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings


admin.autodiscover()

if settings.DEBUG:
    try:
        import thweddy.wingdbstub
    except ImportError:
        pass

urlpatterns = patterns('',
    (r'^', include('thweddy.main.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_DOC_ROOT}),
    (settings.ADMIN_URL, include(admin.site.urls)),
)
