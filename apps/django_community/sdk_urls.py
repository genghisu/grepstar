from django.conf.urls.defaults import *

urlpatterns = patterns('django_community.sdk_views',
    url(r'^login/$', 'login', name='sdk-login'),
    url(r'^register/$', 'register', name='sdk-register'),
    url(r'^logout/$', 'logout', name='sdk-logout'),
)