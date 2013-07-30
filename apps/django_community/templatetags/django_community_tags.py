from django import template
from django.template import Node, NodeList, Template, Context, Variable, VariableDoesNotExist
from django.template.defaulttags import IfEqualNode
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.template.loader import render_to_string

from django_utils.templatetag_helpers import resolve_variable, copy_context
from django_community.models import Favorite, UserProfile

register = template.Library()
    
@register.tag(name="favorites")
def do_favorites(parser,  token):
    """
    @object - object to return the favorite count for
    """
    try:
        tag, object  = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError,  "%r tag requires one argument" % token.contents.split()[0]
    return ModelFavorites(object)

class ModelFavorites(template.Node):
    def __init__(self, object):
        self.object = object
        
    def render(self,  context):
        object = resolve_variable(self.object, context, self.object)
        favorites = Favorite.objects.favorites_for_object(object)
        object.favorites = favorites
        return favorites

@register.tag(name="associate_favorite_status")
def do_associate_favorite(parser, token):
    """
    @object - object to return the favorite count for
    """
    try:
        tag, node, user  = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError,  "%r tag requires one argument" % token.contents.split()[0]
    return AssociateFavorite(node, user)

class AssociateFavorite(template.Node):
    def __init__(self, node, user):
        self.node = node
        self.user = user
        
    def render(self,  context):
        user = resolve_variable(self.user, context, self.user)
        node = resolve_variable(self.node, context, self.node)
        node.already_favorited = Favorite.objects.favorites_for_object(node).filter(user = user)
        return ''