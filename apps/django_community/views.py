import json

import django.http as http
import django.shortcuts as shortcuts
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

import django_community.models
import django_community.utils
import django_community.forms
from django_utils.pagination import paginate_queryset, paginate_queryset_ajax
from django_utils import request_helpers
import django_utils.pagination as pagination
import django_community.decorators as django_community_decorators
import django_community.config as app_config
from django_community.utils import handle_registration, handle_login, check_firstname, check_lastname, check_website, check_aboutme
from django_community.forms import LoginForm, SignupForm, build_edit_profile_form

def edit_profile(request):
    EditProfileForm = build_edit_profile_form(request.user)
    
    if request.POST:
        form = EditProfileForm(request.POST)
        if form.is_valid():
            pass
    else:
        form = EditProfileForm()
        
    return shortcuts.render_to_response(
        'web/auth/edit_profile.html', 
        {'form':form}, 
        context_instance = RequestContext(request),
    )
        
def profile(request, username):
    """
    Gathers and displays user profile data.
    """
    try:
        user = User.objects.get(username = username)
    except ObjectDoesNotExist:
        return http.HttpResponseNotFound()
    
    most_popular_assets = Asset.objects.filter(complete = True, deleted = False, user = user).order_by('-date_created')
    for asset in most_popular_assets:
        asset.trunc_comments = asset.comments.all()[0:5]
        asset.target_width, asset.target_height = asset.fit_to_width(256)
            
    context = {}
    context['is_owner'] = request.user == user
    context['user'] = user
    context['assets'] = most_popular_assets
    
    return shortcuts.render_to_response(
        'web/auth/profile.html', 
        context, 
        context_instance = RequestContext(request),
    )

def ajax_signup_complete(request):
    errors = []
    results = {}
    
    aboutme = request.POST.get('aboutme', '').strip()
    website = request.POST.get('website', '').strip()
    firstname = request.POST.get('firstname', '').strip()
    lastname = request.POST.get('lastname', '').strip()

    check_firstname(firstname)
    check_lastname(lastname)
    check_website(website)
    check_aboutme(aboutme)

    if request.user and request.user.is_authenticated():
        request.user.profile.update_profile(firstname, lastname, website, aboutme)
    else:
        errors.append('LOGIN_REQUIRED')
    
    response = {'status':not(bool(errors)), 'errors':errors, 'results':results}
    
    return shortcuts.render_to_response('json.html',
                                        {'response':json.dumps(response)},
                                        context_instance = RequestContext(request)) 

def ajax_signup(request):
    params = request.POST
    results = {}
    errors = []
    
    username = params.get('username', '').strip()
    password = params.get('password', '').strip()
    email = params.get('email', '').strip()
    
    cleaned_data = {'username':username,
                    'email':email,
                    'password':password,
                    'firstname':'',
                    'lastname':''}
    
    errors = django_community.utils.check_registration(cleaned_data)
    
    if not errors:
        handle_registration(request, cleaned_data)
        results = {'avatar_url':request.user.profile.get_avatar_url(),
                   'username':request.user.username,
                   'profile_url':reverse('site-user-profile', args=[request.user.username])
                   }
        
    response = {'status':not(bool(errors)), 'errors':errors, 'results':results}
    
    if errors:
        response = shortcuts.render_to_response('json.html',
                                                 {'response':json.dumps(response)},
                                                 context_instance = RequestContext(request))
        response.status_code = 500
        return response
    else:
        return shortcuts.render_to_response('fragments/signed_in_header.html',
                                            results,
                                            context_instance = RequestContext(request))
    
def ajax_signin(request):
    params = request.POST
    results = {}
    errors = []
    username = params.get('username', '').strip()
    password = params.get('password', '').strip()
    cleaned_data = {'username':username, 'password':password}
    status = False
    
    if not username:
        errors.append("Please enter a valid username.")
    if not password:
        errors.append("The password cannot be empty.")
    
    if not errors:
        if django_community.utils.check_login(cleaned_data):
            errors.append("Invalid username/email and password combination.")
        else:
            handle_login(request, cleaned_data)
            results = {'avatar_url':request.user.profile.get_avatar_url(),
                       'username':request.user.username,
                       'profile_url':reverse('site-user-profile', args=[request.user.username])}
            status = True
            
    response = {'status':status, 'errors':errors, 'results':results}
    
    if errors:
        response =  shortcuts.render_to_response('json.html',
                                                 {'response':json.dumps(response)},
                                                 context_instance = RequestContext(request))
        response.status_code = 500
        return response
    else:
        return shortcuts.render_to_response('fragments/signed_in_header.html',
                                            results,
                                            context_instance = RequestContext(request))

def ajax_signout(request):
    django_community.utils.handle_signout(request)
    response = {'status':True}
    
    return shortcuts.render_to_response('fragments/signed_out_header.html',
                                        response,
                                        context_instance = RequestContext(request))
    
def standard_signin(request):
    """
    Handles login for none OpenID users.
    """
    path = request_helpers.get_redirect_path(request)
    if request.POST:
        form = LoginForm(request.POST)
        if form.is_valid():
            handle_login(request, form.cleaned_data)
            return http.HttpResponseRedirect(reverse('site-home'))
    else:
        form = LoginForm()
        
    return shortcuts.render_to_response('signin.html',
                                        {'form':form,
                                         'redirect':path},
                                        context_instance = RequestContext(request))

def standard_signup(request):
    """
    Handles signup for none OpenID users.
    """
    path = request_helpers.get_redirect_path(request)
    if request.POST:
        form = SignupForm(request.POST)
        if form.is_valid():
            handle_registration(request, form.cleaned_data)
            return http.HttpResponseRedirect(path)
    else:
        form = SignupForm()
    
    return shortcuts.render_to_response('web/auth/signup.html',
                                        {'form':form,
                                         'redirect':path},
                                        context_instance = RequestContext(request))

def signout(request):
    django_community.utils.handle_signout(request)
    path = request_helpers.get_redirect_path(request)
    if path.strip():
        return http.HttpResponseRedirect(reverse('site-home'))
    else:
        return http.HttpResponseRedirect(reverse('site-home'))