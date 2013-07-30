from django.conf.urls.defaults import *

urlpatterns = patterns('django_community.views',
    url(r'^ajax_signin/$', 'ajax_signin', name='ajax-signin'),
    url(r'^ajax_signout/$', 'ajax_signout', name='ajax-signout'),
    url(r'^ajax_signup/$', 'ajax_signup', name='ajax-signup'),
    url(r'^ajax_signup_complete/$', 'ajax_signup_complete', name='ajax-signup-complete'),
    
    url(r'^signin/$', 'standard_signin', name='site-signin'),
    url(r'^signup/$', 'standard_signup', name='site-signup'),
    url(r'^profile/(?P<username>.+)/$', 'profile', name='site-profile'),
    url(r'^signout/$', 'signout', name='site-signout'),
)