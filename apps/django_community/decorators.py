from django import http
from django.core.urlresolvers import reverse
from django.utils.functional import wraps
from django.utils.http import urlquote
from django.views.generic.simple import direct_to_template

import django_community.config as config
import django_community.utils

def UserRequired(func):
    """
    Decorator that redirects the user to the user-required view if they are not logged in.
    
    This function is used for using with view classes that define __call__.
    """
    @wraps(func)
    def dec(target, request, *args, **kwargs):
        if django_community.utils.is_anon_user(request.user) or not request.user.is_authenticated():
            url = reverse('community-combined-login') + '?redirect=%s' % (request.path)
            return http.HttpResponseRedirect(url)
        return func(target, request, *args, **kwargs)
    
    return dec

def user_required(func):
    """
    Decorator that redirects the user to the user-required view if they are not logged in.
    
    This function is used to decorate views in the for of def view(**params).
    """
    @wraps(func)
    def dec(request, *args, **kwargs):
        if django_community.utils.is_anon_user(request.user) or not request.user.is_authenticated():
            url = reverse('community-combined-login') + '?redirect=%s' % (request.path)
            return http.HttpResponseRedirect(url)
        return func(request, *args, **kwargs)
    return dec

def anonymous_required(func):
    """
    Decorator that redirects the user to the anonymous-required view if they are not logged in.
    
    This function is used to decorate views in the for of def view(**params).
    """
    @wraps(func)
    def dec(request, *args, **kwargs):
        if config.ANONYMOUS_USERS_ENABLED and not django_community.utils.is_anon_user(request.user):
            url = reverse('anonymous-required')
            return http.HttpResponseRedirect(url)
        elif config.ANONYMOUS_USERS_ENABLED and request.user.is_authenticated():
            url = reverse('anonymous-required')
            return http.HttpResponseRedirect(url)
        return func(request, *args, **kwargs)
    return dec
