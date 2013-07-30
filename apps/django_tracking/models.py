from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django_extensions.db.fields import CreationDateTimeField, ModificationDateTimeField
from django.core.exceptions import ObjectDoesNotExist

class ViewsManager(models.Manager):
    def views_for_object(self, object):
        content_type_object = ContentType.objects.get_for_model(object.__class__)
        count = self.model.objects.filter(content_type = content_type_object, object_id = object.id).count()
        return count
    
    def add(self, object, ip):
        content_type_object = ContentType.objects.get_for_model(object.__class__)
        view = self.model(content_type = content_type_object, object_id = object.id, ip = ip)
        view.save()
        return view
    
class DownloadsManager(models.Manager):
    def downloads_for_object(self, object):
        content_type_object = ContentType.objects.get_for_model(object.__class__)
        count = self.model.objects.filter(content_type = content_type_object, object_id = object.id).count()
        return count
    
class View(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    ip = models.IPAddressField()
    
    date_created = CreationDateTimeField()
    
    objects = ViewsManager()
    
    def __unicode__(self):
        return "%s::%s" % (self.content_type.model, str(self.ip))
    
class Download(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    
    date_created = CreationDateTimeField()
    user = models.ForeignKey(User)
    
    objects = DownloadsManager()