import datetime
import json

import django.http as http
import django.shortcuts as shortcuts
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from tagging.models import TaggedItem
from django.contrib.auth.models import User
from django.conf import settings

###########################HOME############################
def home(request):
    return shortcuts.render_to_response('home.html',
                                        {},
                                        context_instance = RequestContext(request))
    
def web_projects(request):
    return shortcuts.render_to_response('web_projects.html',
                                        {},
                                        context_instance = RequestContext(request))
    
def contact(request):
    return shortcuts.render_to_response('contact.html',
                                        {},
                                        context_instance = RequestContext(request))
    
def mobile_projects(request):
    return shortcuts.render_to_response('mobile_projects.html',
                                        {},
                                        context_instance = RequestContext(request))