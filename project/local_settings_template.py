from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'picmobo',
        'USER': 'picmobo',
        'PASSWORD': 'picmobo',
        'HOST': 'picmobodb.c4mcfua0hmzs.us-east-1.rds.amazonaws.com',
        'PORT': '3306',
    }
}