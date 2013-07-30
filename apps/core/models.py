# -*- coding: utf-8 -*-
import uuid
import logging
import base64
import re
import json
import pytz
import math

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from django.db.models.signals import post_save

from tagging.models import Tag, TaggedItem
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField

logger = logging.getLogger('django')