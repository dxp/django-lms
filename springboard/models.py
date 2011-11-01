from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group
from djangotoolbox.fields import ListField

class IntranetApplication(models.Model):
    icon = models.ImageField(upload_to = 'images')
    url = models.CharField(max_length = '255')
    title = models.CharField(max_length = '255')
    groups = ListField(models.ForeignKey(Group), blank=True)

    def __unicode__(self):
        return self.title
