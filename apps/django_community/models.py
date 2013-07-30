import datetime

from django.utils.translation import ugettext as _
from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django_utils.request_helpers import get_ip
from django.core.exceptions import ObjectDoesNotExist