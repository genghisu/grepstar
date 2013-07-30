from django.conf import settings

def analytics(request):
    """
    Exposes variables for web analytics
    
    @var google_analytics_key - Google Analytics Key
    """
    
    key = settings.GOOGLE_ANALYTICS_KEY

    if not settings.DEBUG:
    	return {'GOOGLE_ANALYTICS_KEY':key}
    else:
    	return {'GOOGLE_ANALYTICS_KEY':''}
