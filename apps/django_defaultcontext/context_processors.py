from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist

def defaults(request):
    default_context = {}
    default_context['STATIC_URL'] = settings.STATIC_URL

    return default_context