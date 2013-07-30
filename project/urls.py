from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'core.views.home', name='site-home'),
    url(r'^web/$', 'core.views.web_projects', name='site-web-projects'),
    url(r'^contact/$', 'core.views.contact', name='site-contact'),
    url(r'^mobile/$', 'core.views.mobile_projects', name='site-mobile-projects'),
)

if getattr(settings, 'LOCAL_DEV_SERVER', None):
    from urlparse import urlsplit    
    url = urlsplit(settings.MEDIA_URL).path[1:]
    root = settings.MEDIA_ROOT
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % url, 'serve', {'document_root': root, 'show_indexes': True}),
    )
    url = urlsplit(settings.STATIC_URL).path[1:]
    root = settings.STATIC_ROOT
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % url, 'serve', {'document_root': root, 'show_indexes': True}),
    )
    url = urlsplit(settings.STATIC_LOCAL_URL).path[1:]
    root = settings.STATIC_LOCAL_ROOT
    urlpatterns += patterns('django.views.static',
        (r'^%s(?P<path>.*)$' % url, 'serve', {'document_root': root, 'show_indexes': True}),
    )
    

