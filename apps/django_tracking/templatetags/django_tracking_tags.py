from django import template
from django.template import Node, NodeList, Template, Context, Variable, VariableDoesNotExist
from django.template.defaulttags import IfEqualNode
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string

from django_utils.templatetag_helpers import resolve_variable, copy_context
from django_tracking.models import View, Download

register = template.Library()

@register.tag(name="views")
def do_get_views(parser,  token):
    """
    @object - object to return the view count for
    """
    try:
        tag, object  = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError,  "%r tag requires one argument" % token.contents.split()[0]
    return ModelViews(object)

class ModelViews(template.Node):
    """
    TODO
    """
    
    def __init__(self, object):
        self.object = object
        
    def render(self,  context):
        object = resolve_variable(self.object, context, self.object)
        views = View.objects.views_for_object(object)
        object.views = views
        return views

@register.tag(name="downloads")
def do_get_downloads(parser, token):
    """
    @object - object to return the download count for
    """
    try:
        tag, object  = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError,  "%r tag requires one argument" % token.contents.split()[0]
    return ModelDownloads(object)

class ModelDownloads(template.Node):
    """
    TODO
    """
    
    def __init__(self, object):
        self.object = object
        
    def render(self,  context):
        object = resolve_variable(self.object, context, self.object)
        views = Download.objects.views_for_object(object)
        object.downloads = downloads
        return downloads