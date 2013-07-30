from django_utils.request_helpers import get_ip

def community(request):
    """
    Exposes authentication context variables.
    
    @var community_user - User who is currently logged in, None if no one is logged in.
    @var islogged - True if a user is logged in.
    @var isAnon - True if an anonymous user is using the site.
    """
    user = request.user
    
    return {'community_user':user,  
    		'islogged':user.is_authenticated(), 
    		'is_admin':user.is_superuser
            }