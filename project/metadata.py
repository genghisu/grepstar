import os

try:
    from __revision__ import __revision__
except:
    __revision__ = 'develop'

metadata = {
    'name': "hanbox",
    'version': "1.0",
    'release': __revision__,
    'url': 'http://hanbox.org',
    'author': 'Han Mdarien',
    'author_email': 'han.mdarien@gmail.com',
    'admin': 'han.mdarien@gmail.com',
    'dependencies': (
        'django-haystack',
        'South',
        'django-extensions',
        'html5lib',
        'pysolr',
        'boto',
        'pytz',
        'oauth2',
	    'python-memcached',
    ),
    'description': '',
    'license': 'Private',
}
