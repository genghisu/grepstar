import datetime

from django_community.config import ANONYMOUS_USERS_ENABLED
from django_community.models import UserOpenID, UserProfile
from django_community.utils import create_user_from_openid, get_anon_user, is_anon_user, process_ax_data
from django.core.exceptions import ObjectDoesNotExist

class CommunityMiddleware(object):
    """
    Attaches user profile data to authenticated users.
    """
    def process_request(self, request):
        if request.user.is_authenticated():
            request.user.profile = UserProfile.objects.get_user_profile(request.user)
            request.user.last_login = datetime.datetime.now()
            request.user.save()

