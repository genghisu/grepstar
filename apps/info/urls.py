from django.conf.urls.defaults import *

urlpatterns = patterns('info.views',
    url(r'^faq/', 'faq',  name='info-faq'), 
    url(r'^about/', 'about',  name='info-about'), 
    url(r'^tos/', 'tos',  name='info-tos'),
    url(r'^privacy/', 'privacy',  name='info-privacy'),  
    url(r'^contact/', 'contact',  name='info-contact'),
    url(r'^feedback/', 'feedback',  name='info-feedback'),
    url(r'^markdown/',  'markdown',  name='info-markdown'), 
    url(r'^reputation/',  'reputation',  name='info-reputation'), 
    url(r'^htmltags/',  'htmltags',  name='info-htmltags'), 
)
