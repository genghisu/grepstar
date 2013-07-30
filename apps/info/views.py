import django.http as http
import django.shortcuts as shortcuts
from django.core.urlresolvers import reverse
from django.template import RequestContext

def tos(request):
    return shortcuts.render_to_response('info/tos.html',  {},  context_instance = RequestContext(request))
    
def about(request):
    return shortcuts.render_to_response('info/about.html',  {},  context_instance = RequestContext(request))

def privacy(request):
    return shortcuts.render_to_response('info/privacy.html',  {},  context_instance = RequestContext(request))

def faq(request):
    return shortcuts.render_to_response('info/faq.html',  {},  context_instance = RequestContext(request))
    
def contact(request):
    return shortcuts.render_to_response('info/contact.html',  {},  context_instance = RequestContext(request))
    
def feedback(request):
    return shortcuts.render_to_response('info/feedback.html',  {},  context_instance = RequestContext(request))