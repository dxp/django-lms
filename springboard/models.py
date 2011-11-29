from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from djangotoolbox.fields import ListField, ForeignKey

class IntranetApplication(models.Model):
    icon = models.ImageField(upload_to = 'images')
    url = models.CharField(max_length = '255')
    title = models.CharField(max_length = '255')
    # TODO: Fix MongoDB backend to handle this as a ListField(ForeignKey())
    groups = ListField(ForeignKey(Group, related_name="test"), blank=True)
    #group = models.ForeignKey(Group)
    # groups = ListField(models.CharField(max_length="24"), blank=True)

    def __unicode__(self):
        return self.title
