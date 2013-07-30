import json
import logging

import django.http as http
import django.shortcuts as shortcuts
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import logout as auth_logout

from django_community.utils import check_login, handle_login, check_registration, handle_registration
from core.models import AppUsage
from core.utils import validate_request, complete_errors

logger = logging.getLogger('django')

def logout(request):
    response = {}
    
    errors = validate_request(request, False, True, True)
    if not errors:
        auth_logout(request)
    
    if not errors:
        response = {'success':True}
    else:
        response = {'errors':errors}
        
    return shortcuts.render_to_response('json.html',
                                        {'response': json.dumps(response)},
                                        context_instance = RequestContext(request),
                                        mimetype = "application/json")
    
def login(request):
    response = {}
    
    errors = validate_request(request, False, True, True)
    
    if not errors:
        errors += check_login(request, request.POST)
        if not errors:
            user = handle_login(request, request.POST)
    
    if not errors:
        AppUsage.objects.add_app_usage(user, request.POST.get('api_key'))
        user_dict = user.profile.logged_user_details_as_dict()
        response = {'success':True, 'user':user_dict}
    else:
        response = {'errors':errors}
        
    return shortcuts.render_to_response('json.html',
                                        {'response': json.dumps(response)},
                                        context_instance = RequestContext(request),
                                        mimetype = "application/json")

def register(request):
    errors = validate_request(request, False, True, True)
    
    if not errors:
        errors += check_registration(request, request.POST)
        if not errors:
            user = handle_registration(request, request.POST)
    
    if not errors:
        AppUsage.objects.add_app_usage(user, request.POST.get('api_key'))
        user_dict = user.profile.logged_user_details_as_dict()
        response = {'success':True, 'user':user_dict}
    else:
        response = {'errors':errors}
        
    return shortcuts.render_to_response('json.html',
                                        {'response': json.dumps(response)},
                                        context_instance = RequestContext(request),
                                        mimetype = "application/json")